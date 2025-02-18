from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from utils.sse import sse_manager

router = APIRouter()

@router.get("/api/push-events")
async def push_events():
    """
    SSE endpoint for pushing real-time updates to the frontend.
    """
    return StreamingResponse(sse_manager.register(), media_type="text/event-stream")
