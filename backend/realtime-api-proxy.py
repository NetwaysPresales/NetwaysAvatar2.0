import os
import asyncio
import websockets
import websockets.headers
from fastapi import FastAPI, WebSocket
from fastapi.responses import JSONResponse
from fastapi.websockets import WebSocketDisconnect
from dotenv import load_dotenv

load_dotenv()

# Configuration
AZURE_OPENAI_REALTIME_ENDPOINT = os.getenv('AZURE_OPENAI_REALTIME_ENDPOINT')
AZURE_OPENAI_REALTIME_KEY = os.getenv('AZURE_OPENAI_REALTIME_KEY')
LOCALPORT = int(os.getenv('LOCALPORT', 5050))

app = FastAPI()

if not AZURE_OPENAI_REALTIME_KEY:
    raise ValueError('Missing the OpenAI API key. Please set it in the .env file.')

@app.get("/", response_class=JSONResponse)
async def index_page():
    return {"message": "OpenAI Realtime API Interface is running!"}

@app.websocket("/realtime-api")
async def realtime_api_proxy(websocket: WebSocket):
    """Proxy WebSocket connections between clients and OpenAI Realtime API."""
    await websocket.accept()
    
    async with websockets.connect(
        AZURE_OPENAI_REALTIME_ENDPOINT+f'&api-key={AZURE_OPENAI_REALTIME_KEY}'
    ) as openai_ws:
        
        async def receive_from_client():
            """Relay messages from client to OpenAI."""
            try:
                async for message in websocket.iter_text():
                    await openai_ws.send(message)
            except WebSocketDisconnect:
                await openai_ws.close()

        async def send_to_client():
            """Relay messages from OpenAI to client."""
            try:
                async for message in openai_ws:
                    await websocket.send_text(message)
            except Exception as e:
                print(f"Error in send_to_client: {e}")

        await asyncio.gather(receive_from_client(), send_to_client())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=LOCALPORT)
