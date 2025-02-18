from fastapi import WebSocket, WebSocketDisconnect, APIRouter
import json
from data_models.settings_model import Settings, current_settings
from logger import logger

router = APIRouter()

@router.websocket("/ws/settings")
async def settings_websocket(websocket: WebSocket):
    await websocket.accept()
    try:
        # Immediately push the current settings to the client
        await websocket.send_text(json.dumps(current_settings.dict()))
        logger.info("Pushed initial settings to client.")
        
        while True:
            # Wait for an update from the client
            data = await websocket.receive_text()
            new_settings = json.loads(data)
            # Overwrite current settings (or merge, if desired)
            current_settings = Settings(**new_settings)
            logger.info("Received updated settings from client: %s", new_settings)
            # Optionally push back confirmation or the new settings
            await websocket.send_text(json.dumps(current_settings.dict()))
            
    except WebSocketDisconnect:
        logger.info("Settings websocket disconnected.")
