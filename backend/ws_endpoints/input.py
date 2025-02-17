import base64
import json
from fastapi import WebSocket
from utils.azure_connection import connect_to_azure
from logger import logger

async def websocket_input(websocket: WebSocket):
    await websocket.accept()
    logger.info("Client connected to /ws/input")
    try:
        azure_connection = await connect_to_azure()
        while True:
            data = await websocket.receive_bytes()
            audio_b64 = base64.b64encode(data).decode("utf-8")
            message = {"type": "input_audio_buffer.append", "data": audio_b64}
            await azure_connection.send(json.dumps(message))
    except Exception as e:
        logger.error("Error in /ws/input: %s", e)
    finally:
        await websocket.close()
