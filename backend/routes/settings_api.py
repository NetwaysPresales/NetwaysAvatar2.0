from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, StreamingResponse
import asyncio
from data_models.settings_model import current_settings, Settings
from logger import logger

router = APIRouter()

@router.put("/api/update-settings")
async def update_settings(request: Request):
    """
    Updates system settings with validated data.
    """
    try:
        new_settings = await request.json()
        validated_settings = Settings(**new_settings)  # Validate incoming data
        global current_settings
        current_settings = validated_settings  # Store validated settings
        logger.info("Updated settings: %s", current_settings.model_dump_json())
        return JSONResponse(content={"message": "Settings updated successfully"})
    except Exception as e:
        logger.error("Error updating settings: %s", e)
        return JSONResponse(status_code=400, content={"message": "Invalid settings format"})

@router.get("/api/push-settings")
async def push_settings(request: Request):
    """
    SSE endpoint to push validated settings updates.
    """
    async def event_generator():
        while True:
            await asyncio.sleep(5)
            yield f"data: {current_settings.model_dump_json()}\n\n"
    return StreamingResponse(event_generator(), media_type="text/event-stream")
