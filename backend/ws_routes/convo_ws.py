import asyncio
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from data_models.state_model import current_state
from data_models.settings_model import current_settings
from logger import logger
from ws_routes.openai_ws import get_openai_ws, reset_openai_ws
from ws_routes.data_sync_ws import update_state_param

router = APIRouter()

async def handle_input_message(message: dict, openai_ws: WebSocket) -> None:
    """
    Processes a message from the client.
    If text is provided, sends a conversation.item.create event.
    If binary data is provided, sends an input_audio_buffer.append event.
    """
    match message:
        case {"text": text_data}:
            text_data = text_data.strip()
            if text_data:
                conv_item_payload = {
                    "type": "conversation.item.create",
                    "item": {
                        "type": "message",
                        "content": [{
                            "type": "input_text",
                            "text": text_data
                        }],
                        "role": "user"
                    }
                }
                await openai_ws.send(json.dumps(conv_item_payload))
                logger.info("Sent conversation.item.create to OpenAI: %s", conv_item_payload)
                
                # Immediately request a response using current settings.
                response_payload = {
                    "type": "response.create",
                    "response": {
                        "modalities": ["text", "audio"],
                        "instructions": current_settings.get_instruction_prompt_formatted(),
                        "voice": current_settings.openai.voice,
                        "output_audio_format": "pcm16",
                        "tools": [tool.model_dump() for tool in current_settings.app.enabled_tools],
                        "tool_choice": "auto",
                        "temperature": current_settings.openai.temperature,
                        "max_output_tokens": current_settings.openai.max_tokens
                    }
                }
                await openai_ws.send(json.dumps(response_payload))
                logger.info("Sent response.create to OpenAI: %s", response_payload)
        case {"audio_bytes": data_b64}:
            payload = {"type": "input_audio_buffer.append", "data": data_b64}
            await openai_ws.send(json.dumps(payload))
            logger.info("Forwarded audio chunk to OpenAI.")
        case _:
            logger.warning("Received unknown message type from client: %s", message)

async def process_openai_event(response: str, websocket: WebSocket) -> None:
    """
    Processes an event received from OpenAI, updates the conversation state,
    forwards the event to the client, and updates the frontend via the data sync WS
    using the update functions.
    """
    try:
        response_json = json.loads(response)
    except json.JSONDecodeError:
        logger.error("Invalid JSON received from OpenAI: %s", response)
        return

    event_type = response_json.get("type")
    update_state_param("last_event", event_type)

    match event_type:
        case "session.created":
            update_state_param("session_active", True)
            update_state_param("session_id", response_json.get("session_id"))
            await websocket.send_text(response)
            logger.info("Session created. Session ID: %s", current_state.session_id)
        case "conversation.item.created":
            conv_id = response_json.get("conversation_id")
            if conv_id:
                update_state_param("conversation_id", conv_id)
                logger.info("Conversation created. Conversation ID: %s", conv_id)
            await websocket.send_text(response)
        case "response.audio.delta":
            await websocket.send_text(response)
            logger.info("Sent AI audio chunk to client.")
        case "response.audio_transcript.delta":
            await websocket.send_text(response)
            logger.info("Sent transcript delta to client.")
        case "speech_started":
            update_state_param("speech_detected", True)
            await websocket.send_text(response)
            logger.info("Speech started detected; instructing client to reset playback.")
        case "speech_ended":
            update_state_param("speech_detected", False)
            await websocket.send_text(response)
            logger.info("Speech ended detected; resuming playback.")
        case "response.done":
            update_state_param("response_active", False)
            await websocket.send_text(response)
            logger.info("AI response completed.")
        case _:
            await websocket.send_text(response)
            logger.info("Forwarded event from OpenAI: %s", response_json)

async def forward_input(websocket: WebSocket, openai_ws: WebSocket) -> None:
    """
    Continuously receives messages from the client and processes them.
    """
    while True:
        try:
            data = await websocket.receive_text()
            # parse and handle the incoming message
            message = json.loads(data)
            await handle_input_message(message, openai_ws)

        except WebSocketDisconnect:
            # The client disconnected; stop reading further messages
            logger.info("Client disconnected from convo WebSocket.")
            break

        except Exception as e:
            logger.error("Error processing input message: %s", e)
            # Decide whether you want to break or continue
            break

async def forward_output(websocket: WebSocket, openai_ws: WebSocket) -> None:
    """
    Continuously receives messages from OpenAI and processes them.
    """
    while True:
        response = await openai_ws.recv()
        await process_openai_event(response, websocket)

@router.websocket("/ws/convo")
async def convo_ws(websocket: WebSocket) -> None:
    """
    Consolidated conversation WebSocket endpoint.
    Manages both incoming messages from the client and outgoing messages from OpenAI.
    If a disconnect is detected, resets the OpenAI connection.
    """
    await websocket.accept()
    logger.info("Client connected to /ws/convo")
    try:
        openai_ws = await get_openai_ws()
        await asyncio.gather(
            forward_input(websocket, openai_ws),
            forward_output(websocket, openai_ws)
        )
    except WebSocketDisconnect:
        logger.info("Client disconnected from /ws/convo. Resetting OpenAI connection.")
        await reset_openai_ws()
    except Exception as e:
        logger.error("Error in /ws/convo: %s", e)
