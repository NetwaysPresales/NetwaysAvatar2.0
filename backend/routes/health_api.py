from fastapi import APIRouter
from logger import logger

router = APIRouter()

@router.get("/health")
async def health_check():
    """
    Health check endpoint to ensure the server is running.
    """
    logger.info("Health check requested.")
    return {"status": "running", "message": "Proxy server is alive"}
