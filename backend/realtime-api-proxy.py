import asyncio
import os
import json
import logging
import websockets
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

# Load environment variables
load_dotenv()

AZURE_OPENAI_REALTIME_ENDPOINT = os.getenv('AZURE_OPENAI_REALTIME_ENDPOINT')
AZURE_OPENAI_REALTIME_KEY = os.getenv('AZURE_OPENAI_REALTIME_KEY')

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("proxy_server.log"),  # Save logs to file
      #  logging.StreamHandler()  # Print logs to console
    ]
)

logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/health")
async def health_check():
    """
    Health check endpoint to ensure the server is running.
    """
    logger.info("Health check requested.")
    return {"status": "running", "message": "Proxy server is alive"}

@app.websocket("/ws")
async def websocket_proxy(websocket: WebSocket):
    """
    WebSocket proxy that sends a text query to Azure OpenAI and streams back text and audio responses.
    """
    await websocket.accept()
    logger.info("Frontend WebSocket connected.")

    try:
        async with websockets.connect(
            AZURE_OPENAI_REALTIME_ENDPOINT,
            additional_headers={"api-key": AZURE_OPENAI_REALTIME_KEY}
        ) as azure_ws:
            logger.info("Connected to Azure OpenAI WebSocket.")

            # Wait for 'session.created' event
            try:
                session_created = await azure_ws.recv()
                logger.info("Azure Session Created.")
                await websocket.send_text(session_created)  # Send to frontend
            except Exception as e:
                logger.error(f"Error receiving 'session.created': {e}")
                await websocket.close()
                return

            # Send session.update to Azure
            session_update = {
                "type": "session.update",
                "session": {
                    "turn_detection": {"type": "server_vad"},
                    "input_audio_format": "pcm16",
                    "output_audio_format": "pcm16",
                    "voice": "alloy",
                    "instructions": "You are a helpful AI assistant.",
                    "modalities": ["text", "audio"],
                    "temperature": 0.8
                }
            }
            await azure_ws.send(json.dumps(session_update))
            logger.info("Sent session.update to Azure.")

            # Wait for response from session.update
            session_update_response = await azure_ws.recv()
            logger.info(f"Received response for session.update: {json.dumps(json.loads(session_update_response), separators=(',', ':'))}")

            # Send a text query as a conversation item
            conversation_item = {
                "type": "conversation.item.create",
                "item": {
                    "type": "message",  
                    "role": "user",     
                    "content": [
                        {
                            "type": "input_text",  
                            "text": "Hello! Can you tell me a fun fact about space?"
                        }
                    ]
                }
            }
            await azure_ws.send(json.dumps(conversation_item))
            logger.info("Sent conversation.item.create to Azure.")

            # Wait for response from conversation.item.create
            conversation_item_response = await azure_ws.recv()
            logger.info(f"Received response for conversation.item.create: {json.dumps(json.loads(conversation_item_response), separators=(',', ':'))}")

            # Send response.create to start processing
            response_create = {"type": "response.create"}
            await azure_ws.send(json.dumps(response_create))
            logger.info("Sent response.create to Azure.")

            # Wait for response from response.create
            response_create_response = await azure_ws.recv()
            logger.info(f"Received response for response.create: {json.dumps(json.loads(response_create_response), separators=(',', ':'))}")

            # Variable to store transcribed text chunks
            transcribed_text = ""

            async def from_azure_to_client():
                nonlocal transcribed_text
                while True:
                    try:
                        response = await azure_ws.recv()
                        response_json = json.loads(response)

                        # Process text transcripts (concatenating delta)
                        if response_json.get("type") == "response.audio_transcript.delta":
                            delta_text = response_json.get("delta", "")
                            transcribed_text += delta_text
                            logger.info(f"Transcribed Text Delta: {delta_text}")

                            # Stream text delta to frontend
                            await websocket.send_text(json.dumps({"type": "text", "content": delta_text}))

                        # Process audio chunks
                        elif response_json.get("type") == "response.audio.delta":
                            audio_chunk = response_json.get("delta")
                            if audio_chunk:
                                logger.info(f"Streaming audio chunk of size: {len(audio_chunk)} bytes")
                                await websocket.send_bytes(audio_chunk)  # Send audio to client

                        # Log and forward other responses
                        else:
                            logger.info(f"Received non-audio response: {json.dumps(response_json, separators=(',', ':'))}")
                            await websocket.send_text(response)

                    except websockets.exceptions.ConnectionClosed:
                        logger.warning("Azure WebSocket connection closed.")
                        break
                    except Exception as e:
                        logger.error(f"Error receiving from Azure: {e}")
                        break

            await from_azure_to_client()

    except Exception as e:
        logger.error(f"Proxy error: {e}")
        await websocket.close()
