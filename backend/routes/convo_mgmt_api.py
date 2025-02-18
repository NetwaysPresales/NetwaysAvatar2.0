import json
import asyncio
from fastapi import APIRouter, WebSocket
from fastapi.responses import JSONResponse
from data_models.settings_model import current_settings
from data_models.state_model import current_state
from logger import logger
from backend.utils.openai_connection import connect_to_realtime_api, send_ws_message
from utils.sse import SSEManager

router = APIRouter()
sse_manager = SSEManager()  # Manage SSE connections
azure_ws = None  # Global WebSocket connection

@router.get("/api/start-session")
async def start_session():
    """Starts a new session if one isn't already active."""
    global azure_ws

    if current_state.session_active:
        return JSONResponse(status_code=400, content={"message": "Session already active."})

    try:
        azure_ws = await connect_to_realtime_api()
        current_state.session_active = True
        logger.info("Session started.")

        session_update = {
            "type": "session.update",
            "session": {
                "turn_detection": {"type": "server_vad"} if current_settings.vad.server_vad else None,
                "input_audio_format": "pcm16",
                "output_audio_format": "pcm16",
                "voice": current_settings.openai.voice,
                "instructions": current_settings.app.instruction_prompt,
                "modalities": ["text", "audio"],
                "temperature": current_settings.openai.temperature
            }
        }
        await send_ws_message(azure_ws, session_update)

        return JSONResponse(content={"message": "Session started."})
    
    except Exception as e:
        logger.error("Error starting session: %s", e)
        return JSONResponse(status_code=500, content={"message": "Failed to start session."})


@router.get("/api/end-session")
async def end_session():
    """Ends the current session and closes WebSocket connection."""
    global azure_ws

    if not current_state.session_active:
        return JSONResponse(status_code=400, content={"message": "No active session to end."})

    try:
        current_state.session_active = False
        current_state.response_active = False
        current_state.audio_streaming = False
        current_state.waiting_for_commit = False
        current_state.speech_detected = False

        if azure_ws:
            await azure_ws.close()
            azure_ws = None

        logger.info("Session ended.")
        return JSONResponse(content={"message": "Session ended."})
    
    except Exception as e:
        logger.error("Error ending session: %s", e)
        return JSONResponse(status_code=500, content={"message": "Failed to end session."})


@router.get("/api/start-response")
async def start_response():
    """Triggers AI response generation."""
    global azure_ws

    if not current_state.session_active:
        return JSONResponse(status_code=400, content={"message": "No active session."})

    try:
        response_create = {"type": "response.create"}
        await send_ws_message(azure_ws, response_create)

        current_state.response_active = True
        logger.info("AI response started.")
        return JSONResponse(content={"message": "AI response started."})
    
    except Exception as e:
        logger.error("Error starting response: %s", e)
        return JSONResponse(status_code=500, content={"message": "Failed to start response."})


@router.get("/api/end-response")
async def end_response():
    """Stops AI response generation."""
    global azure_ws

    if not current_state.response_active:
        return JSONResponse(status_code=400, content={"message": "No response to cancel."})

    try:
        cancel_event = {"type": "response.cancel"}
        await send_ws_message(azure_ws, cancel_event)

        current_state.response_active = False
        logger.info("AI response cancelled.")
        return JSONResponse(content={"message": "AI response cancelled."})
    
    except Exception as e:
        logger.error("Error cancelling response: %s", e)
        return JSONResponse(status_code=500, content={"message": "Failed to cancel response."})
    
@router.post("/api/commit-audio")
async def commit_audio():
    """
    Commits the input audio buffer.
    """
    try:
        azure_connection = await connect_to_realtime_api()
        commit_message = {"type": "input_audio_buffer.commit"}
        await azure_connection.send(json.dumps(commit_message))
        logger.info("Sent audio commit to Azure.")
        return JSONResponse(content={"message": "Audio commit sent."})
    except Exception as e:
        logger.error("Error sending audio commit: %s", e)
        return JSONResponse(status_code=500, content={"message": "Audio commit failed."})
