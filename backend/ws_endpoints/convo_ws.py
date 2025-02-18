import asyncio
import base64
import json
from fastapi import WebSocket, WebSocketDisconnect
from backend.utils.openai_connection import connect_to_realtime_api  # Your function to connect to Azure
from data_models.state_model import current_state
from logger import logger

async def convo_ws(websocket: WebSocket):
    """
    Consolidated conversation WebSocket endpoint that handles both audio and text input,
    sends messages to the Realtime API, and processes incoming events—updating the conversation
    state (including session_id and conversation_id) as needed.
    """
    await websocket.accept()
    logger.info("Client connected to /ws/convo")
    try:
        azure_ws = await connect_to_realtime_api()

        async def forward_input():
            while True:
                # Receive message from client (could be text or bytes)
                message = await websocket.receive()
                # If it's text input:
                if "text" in message:
                    text_data = message["text"].strip()
                    if text_data:
                        payload = {
                            "type": "conversation.item.create",
                            "item": {
                                "type": "input_text",
                                "text": text_data
                            }
                        }
                        await azure_ws.send(json.dumps(payload))
                        logger.info("Forwarded text input to Azure: %s", text_data)
                # If it's binary audio:
                elif "bytes" in message:
                    data = message["bytes"]
                    audio_b64 = base64.b64encode(data).decode("utf-8")
                    payload = {"type": "input_audio_buffer.append", "data": audio_b64}
                    await azure_ws.send(json.dumps(payload))
                    logger.info("Forwarded audio chunk to Azure.")
                else:
                    logger.warning("Received unknown message type from client: %s", message)

        async def forward_output():
            while True:
                response = await azure_ws.recv()
                try:
                    response_json = json.loads(response)
                except json.JSONDecodeError:
                    logger.error("Invalid JSON received from Azure: %s", response)
                    continue

                event_type = response_json.get("type")
                current_state.last_event = event_type  # Update last event

                # Handle session creation: update session_active flag and session_id
                if event_type == "session.created":
                    current_state.session_active = True
                    current_state.session_id = response_json.get("session_id")
                    await websocket.send_text(response)
                    logger.info("Session created. Session ID: %s", current_state.session_id)

                # Handle conversation creation: update conversation_id if provided
                elif event_type == "conversation.item.created":
                    conv_id = response_json.get("conversation_id")
                    if conv_id:
                        current_state.conversation_id = conv_id
                        logger.info("Conversation created. Conversation ID: %s", conv_id)
                    await websocket.send_text(response)

                # Handle audio response delta
                elif event_type == "response.audio.delta":
                    audio_b64 = response_json.get("delta")
                    if audio_b64:
                        audio_bytes = base64.b64decode(audio_b64)
                        await websocket.send_bytes(audio_bytes)
                        logger.info("Sent AI audio chunk to client.")
                    else:
                        await websocket.send_text(response)

                # Handle transcript delta
                elif event_type == "response.audio_transcript.delta":
                    await websocket.send_text(response)
                    logger.info("Sent transcript delta to client.")

                # Handle speech events
                elif event_type == "speech_started":
                    current_state.speech_detected = True
                    # Notify client (via SSE in your system) to reset playback.
                    # Here we forward the event; the frontend can decide to reset.
                    await websocket.send_text(response)
                    logger.info("Speech started detected.")
                elif event_type == "speech_ended":
                    current_state.speech_detected = False
                    await websocket.send_text(response)
                    logger.info("Speech ended detected.")

                # Handle response completion
                elif event_type == "response.done":
                    current_state.response_active = False
                    await websocket.send_text(response)
                    logger.info("AI response completed.")

                # Handle other events (like errors, cancellation, etc.)
                else:
                    await websocket.send_text(response)
                    logger.info("Forwarded event from Azure: %s", response_json)

        # Run both input and output tasks concurrently
        await asyncio.gather(forward_input(), forward_output())

    except WebSocketDisconnect:
        logger.info("Client disconnected from /ws/convo")
    except Exception as e:
        logger.error("Error in /ws/convo: %s", e)
    finally:
        await websocket.close()
