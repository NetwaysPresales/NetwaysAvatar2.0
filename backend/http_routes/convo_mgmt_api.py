import json
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from data_models.settings_model import current_settings
from data_models.state_model import current_state
from logger import logger
from ws_routes.openai_ws import get_openai_ws, reset_openai_ws, send_session_update

router = APIRouter()
global openai_ws
openai_ws = None

@router.get("/api/start-session")
async def start_session():
    """Starts a new session if one isn't already active."""
    global openai_ws

    if current_state.session_active:
        return JSONResponse(status_code=400, content={"message": "Session already active."})

    try:
        # Get the active OpenAI WebSocket connection (initializes it if needed)
        openai_ws = await get_openai_ws()
        current_state.session_active = True
        logger.info("Session started. Settings: %s", current_settings.model_dump_json())
        
        # Immediately send a session.update with current settings
        await send_session_update()
        logger.info("Sent session.update with configuration.")

        return JSONResponse(content={"message": "Session started."})
    
    except Exception as e:
        logger.error("Error starting session: %s", e)
        return JSONResponse(status_code=500, content={"message": "Failed to start session."})


@router.get("/api/end-session")
async def end_session():
    """Ends the current session and closes WebSocket connection."""
    global openai_ws

    if not current_state.session_active:
        return JSONResponse(status_code=400, content={"message": "No active session to end."})

    try:
        current_state.session_active = False
        current_state.response_active = False
        current_state.speaking_ptt = False
        current_state.waiting_for_commit = False
        current_state.speaking_vad = False

        if openai_ws:
            await openai_ws.close()
            openai_ws = None

        logger.info("Session ended.")
        return JSONResponse(content={"message": "Session ended."})
    
    except Exception as e:
        logger.error("Error ending session: %s", e)
        return JSONResponse(status_code=500, content={"message": "Failed to end session."})


@router.get("/api/start-response")
async def start_response():
    """Triggers AI response generation."""
    global openai_ws

    if not current_state.session_active:
        return JSONResponse(status_code=400, content={"message": "No active session."})

    try:
        response_create = {"type": "response.create"}
        await openai_ws.send(json.dumps(response_create))
        current_state.response_active = True
        logger.info("AI response started.")
        return JSONResponse(content={"message": "AI response started."})
    
    except Exception as e:
        logger.error("Error starting response: %s", e)
        return JSONResponse(status_code=500, content={"message": "Failed to start response."})


@router.get("/api/end-response")
async def end_response():
    """Stops AI response generation."""
    global openai_ws

    if not current_state.response_active:
        return JSONResponse(status_code=400, content={"message": "No response to cancel."})

    try:
        cancel_event = {"type": "response.cancel"}
        await openai_ws.send(json.dumps(cancel_event))
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
    - In push-to-talk mode, called when the user releases the PTT button.
    - In Server VAD mode, committing is automatic.
    """
    global openai_ws

    try:
        if not current_state.session_active:
            return JSONResponse(status_code=400, content={"message": "No active session to commit audio."})
        
        commit_message = {"type": "input_audio_buffer.commit"}
        await openai_ws.send(json.dumps(commit_message))
        logger.info("Audio commit sent to OpenAI.")
        return JSONResponse(content={"message": "Audio commit sent."})
    
    except Exception as e:
        logger.error("Error sending audio commit: %s", e)
        return JSONResponse(status_code=500, content={"message": "Audio commit failed."})
