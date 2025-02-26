import asyncio
import websockets
import json
from config import AZURE_OPENAI_REALTIME_ENDPOINT, AZURE_OPENAI_REALTIME_KEY
from data_models.settings_model import current_settings
from data_models.state_model import current_state
from logger import logger
from ws_routes.data_sync_ws import send_data_sync_update

global _openai_ws
_openai_ws = None
_openai_lock = asyncio.Lock()

def is_ws_connected(ws) -> bool:
    """
    Returns True if the websocket is not None and appears to be open.
    """
    return ws is not None and getattr(ws, "open", False)

async def get_openai_ws():
    """
    Returns the active OpenAI WebSocket connection.
    If none exists or if the connection is closed, initializes a new one.
    """
    global _openai_ws
    async with _openai_lock:
        if not is_ws_connected(_openai_ws):
            logger.info("Connecting to OpenAI WebSocket...")
            _openai_ws = await websockets.connect(
                AZURE_OPENAI_REALTIME_ENDPOINT,
                additional_headers={"api-key": AZURE_OPENAI_REALTIME_KEY}
            )
            logger.info("Connected to OpenAI WebSocket.")
            # Wait for the 'session.created' event from OpenAI.
            try:
                session_created = await _openai_ws.recv()
                logger.info("OpenAI Session Created: %s", session_created)

                # Send session.update with backend settings
                await send_session_update()
                session_updated = await _openai_ws.recv()
                logger.info("OpenAI Session Updated: %s", session_updated[0])

                # Mark the session as active in the state.
                current_state.session_active = True
                # Immediately sync the updated state to the frontend via the data sync WebSocket.
                await send_data_sync_update()
            except Exception as e:
                logger.error("Error receiving session.created: %s", e)
        return _openai_ws

async def send_session_update():
    """
    Sends a session.update event to the OpenAI Realtime API containing the current settings.
    Immediately after sending, it marks the session as active in the global state and
    synchronizes the updated state with the frontend using the data sync WebSocket.
    """
    global _openai_ws
    try:
        payload = {
            "type": "session.update",
            "session": {
                "turn_detection": {
                    "type": "server_vad",
                    "threshold": current_settings.vad.vad_threshold,
                    "prefix_padding_ms": current_settings.vad.vad_prefix_padding,
                    "silence_duration_ms": current_settings.vad.vad_silence_duration,
                    "create_response": current_settings.vad.vad_create_response
                } if current_settings.vad.server_vad else None,
                "tools": [
                    tool.model_dump() for tool in current_settings.app.enabled_tools
                ],
                "tool_choice": "auto",
                "input_audio_format": "pcm16",
                "output_audio_format": "pcm16",
                "voice": current_settings.openai.voice,
                "instructions": current_settings.app.instruction_prompt,
                "modalities": ["text", "audio"],
                "temperature": current_settings.openai.temperature
            }
        }
        await _openai_ws.send(json.dumps(payload))
        logger.info("Sent session.update with configuration: %s", json.dumps(payload))
    except Exception as e:
        logger.error("Error sending session.update: %s", e)

async def reset_openai_ws():
    """
    Resets the OpenAI WebSocket connection by closing the existing one and creating a new one.
    Returns the new connection.
    """
    global _openai_ws
    async with _openai_lock:
        if _openai_ws is not None:
            try:
                await _openai_ws.close()
                logger.info("Closed existing OpenAI WebSocket connection.")
            except Exception as e:
                logger.error("Error closing OpenAI WebSocket: %s", e)
            _openai_ws = None
        
        await get_openai_ws()

        return _openai_ws