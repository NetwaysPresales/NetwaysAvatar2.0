declare global {
    interface Window {
        dataSyncWs: WebSocket | null;
        convoWs: WebSocket | null;
    }
}
  
export {};
  