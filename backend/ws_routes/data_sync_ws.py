import json
import asyncio
from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from data_models.settings_model import current_settings
from data_models.state_model import current_state
from logger import logger

router = APIRouter()
global data_sync_ws
data_sync_ws = None

@router.websocket("/ws/data-sync")
async def data_sync_websocket(websocket: WebSocket):
    await websocket.accept()
    global current_settings, current_state, data_sync_ws
    data_sync_ws = websocket

    # Immediately push the current settings and state to the client
    initial_payload = {
        "settings": current_settings.model_dump(),
        "state": current_state.model_dump()
    }
    await websocket.send_text(json.dumps(initial_payload))
    logger.info("Pushed initial settings and state to client: %s", initial_payload)

    while True:
        try:
            data = await websocket.receive_text()
        except WebSocketDisconnect:
            logger.warning("Data sync websocket disconnected.")
            break  # Break out of the loop once disconnected
        except Exception as e:
            logger.error("Error reading from data-sync websocket: %s", e)
            break

        try:
            update = json.loads(data)
            logger.info("Received sync update from client: %s", update)
            # Process updates using setters
            if "settings" in update:
                # Expecting update["settings"] to be a dict with section names as keys
                for section, updates in update["settings"].items():
                    for param, value in updates.items():
                        update_settings_param(section, param, value)
            if "state" in update:
                # Expecting update["state"] to be a dict with parameter names and values
                for param, value in update["state"].items():
                    update_state_param(param, value)
            
        except Exception as e:
            logger.error("Error processing data-sync update: %s", e)
            # Decide if you want to break or just continue listening for more updates
            break

    # Cleanup after disconnect
    data_sync_ws = None
    logger.info("Data sync websocket loop ended.")

async def send_data_sync_update() -> None:
    global data_sync_ws, current_settings, current_state
    if data_sync_ws:
        payload = {
            "settings": current_settings.dict(),
            "state": current_state.dict()
        }
        try:
            await data_sync_ws.send_text(json.dumps(payload))
            logger.info("Sent data sync update: %s", payload)
        except Exception as e:
            logger.error("Error sending data sync update: %s", e)

async def reset_data_sync_ws():
    global data_sync_ws
    if data_sync_ws:
        try:
            await data_sync_ws.close()
            logger.info("Closed settings sync websocket.")
        except Exception as e:
            logger.error("Error closing settings sync websocket: %s", e)
    data_sync_ws = None

def update_state_param(param: str, value) -> None:
    try:
        # Only update if the new value differs from the current state.
        if getattr(current_state, param, None) == value:
            return
        setattr(current_state, param, value)
        logger.info("Updated state: %s = %s", param, value)
        asyncio.create_task(send_data_sync_update())
    except Exception as e:
        logger.error("Error updating state parameter '%s': %s", param, e)

def update_settings_param(section: str, param: str, value) -> None:
    try:
        current_section = getattr(current_settings, section)
        # Only update if the new value differs.
        if getattr(current_section, param, None) == value:
            return
        setattr(current_section, param, value)
        logger.info("Updated settings: %s.%s = %s", section, param, value)
        asyncio.create_task(send_data_sync_update())
    except Exception as e:
        logger.error("Error updating settings '%s.%s': %s", section, param, e)

