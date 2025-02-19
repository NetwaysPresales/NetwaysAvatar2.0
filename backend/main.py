from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from http_routes.health_api import router as health_router
from http_routes.user_api import router as user_router
from http_routes.convo_mgmt_api import router as convo_mgmt_router
from ws_routes.convo_ws import router as convo_ws_router
from ws_routes.data_sync_ws import router as data_sync_ws_router

# Create the FastAPI app with the WebSocket routes.
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include REST routers.
app.include_router(health_router)
app.include_router(user_router)
app.include_router(convo_mgmt_router)

# Include WebSocket routers.
app.include_router(convo_ws_router)
app.include_router(data_sync_ws_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
