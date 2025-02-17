import json
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from utils.azure_connection import connect_to_azure
from logger import logger

router = APIRouter()

@router.post("/api/commit-audio")
async def commit_audio():
    """
    Commits the input audio buffer.
    """
    try:
        azure_connection = await connect_to_azure()
        commit_message = {"type": "input_audio_buffer.commit"}
        await azure_connection.send(json.dumps(commit_message))
        logger.info("Sent audio commit to Azure.")
        return JSONResponse(content={"message": "Audio commit sent."})
    except Exception as e:
        logger.error("Error sending audio commit: %s", e)
        return JSONResponse(status_code=500, content={"message": "Audio commit failed."})
