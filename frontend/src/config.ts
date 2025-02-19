// Base URL for your backend API
export const BACKEND_DOMAIN = "localhost:8000"

// WebSocket URLs (if needed)
export const WS_CONVO_URL = `ws://${BACKEND_DOMAIN}/ws/convo`;
export const WS_DATA_SYNC_URL = `ws://${BACKEND_DOMAIN}/ws/data-sync`;

// API Endpoints
export const API_ENDPOINTS = {
  health: `http://${BACKEND_DOMAIN}/health`,
  commitAudio: `http://${BACKEND_DOMAIN}/api/commit-audio`,
};
