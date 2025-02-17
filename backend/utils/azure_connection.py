import asyncio
import websockets
import json
from config import AZURE_OPENAI_REALTIME_ENDPOINT, AZURE_OPENAI_REALTIME_KEY
from logger import logger

azure_ws = None
azure_lock = asyncio.Lock()

async def connect_to_azure():
    global azure_ws
    async with azure_lock:
        # Check if there is no connection or if it's not open
        if azure_ws is None or not azure_ws.open:
            logger.info("Connecting to Azure OpenAI WebSocket...")
            azure_ws = await websockets.connect(
                AZURE_OPENAI_REALTIME_ENDPOINT,
                additional_headers={"api-key": AZURE_OPENAI_REALTIME_KEY}
            )
            logger.info("Connected to Azure OpenAI WebSocket.")
            # Wait for the 'session.created' event from Azure.
            try:
                session_created = await azure_ws.recv()
                logger.info("Azure Session Created: %s", session_created)
            except Exception as e:
                logger.error("Error receiving session.created: %s", e)
    return azure_ws

