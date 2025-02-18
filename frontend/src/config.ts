// Base URL for your backend API
export const BACKEND_URL = "http://0.0.0.0:8000";

// WebSocket URLs (if needed)
export const WS_INPUT_URL = "ws://0.0.0.0:8000/ws/input";
export const WS_OUTPUT_URL = "ws://0.0.0.0:8000/ws/output";

// API Endpoints
export const API_ENDPOINTS = {
  health: `${BACKEND_URL}/health`,
  updateSettings: `${BACKEND_URL}/api/update-settings`,
  pushSettings: `${BACKEND_URL}/api/push-settings`,
  userInfo: `${BACKEND_URL}/api/user-info`,
  pushUserInfo: `${BACKEND_URL}/api/push-user-info`,
  conversationSummary: (conversationId: string) =>
    `${BACKEND_URL}/api/conversation-summary/${conversationId}`,
  availableTools: `${BACKEND_URL}/api/available-tools`,
  commitAudio: `${BACKEND_URL}/api/commit-audio`,
};
