import base64
import json
from fastapi import WebSocket
from utils.azure_connection import connect_to_azure
from logger import logger

async def websocket_output(websocket: WebSocket):
    await websocket.accept()
    logger.info("Client connected to /ws/output")
    try:
        azure_connection = await connect_to_azure()
        while True:
            response = await azure_connection.recv()
            response_json = json.loads(response)
            if response_json.get("type") == "response.audio.delta":
                audio_b64 = response_json.get("delta")
                audio_bytes = base64.b64decode(audio_b64)
                await websocket.send_bytes(audio_bytes)
            else:
                await websocket.send_text(response)
    except Exception as e:
        logger.error("Error in /ws/output: %s", e)
    finally:
        await websocket.close()
