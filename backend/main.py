# main.py
from fastapi import FastAPI
from starlette.routing import WebSocketRoute
from backend.routes.health_api import router as health_router
from backend.routes.settings_api import router as settings_router
from backend.routes.user_api import router as user_router
from backend.routes.audio_api import router as audio_router
from ws_endpoints.input import websocket_input
from ws_endpoints.output import websocket_output

# Create WebSocket routes using Starlette's WebSocketRoute.
websocket_routes = [
    WebSocketRoute("/ws/input", endpoint=websocket_input),
    WebSocketRoute("/ws/output", endpoint=websocket_output),
]

# Create the FastAPI app with the WebSocket routes.
app = FastAPI(routes=websocket_routes)

# Include other REST routers.
app.include_router(health_router)
app.include_router(settings_router)
app.include_router(user_router)
app.include_router(audio_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
