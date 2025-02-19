function arrayBufferToBase64(buffer: ArrayBuffer): string {
  let binary = '';
  const bytes = new Uint8Array(buffer);
  const len = bytes.byteLength;
  for (let i = 0; i < len; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return btoa(binary);
}

export class MicStreamer {
    private mediaStream: MediaStream | null = null;
    private mediaRecorder: MediaRecorder | null = null;
    private isStreaming: boolean = false;
  
    constructor(private ws: WebSocket, private micEnabled: () => boolean) {}
  
    async start() {
      if (!navigator.mediaDevices) {
        console.error("Media devices not supported");
        return;
      }
      try {
        this.mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
        this.mediaRecorder = new MediaRecorder(this.mediaStream);
        this.mediaRecorder.ondataavailable = (e: BlobEvent) => {
          if (this.micEnabled()) {
            e.data.arrayBuffer().then((buffer) => {
              if (this.micEnabled() && this.ws.readyState === WebSocket.OPEN) {
                const base64Audio = arrayBufferToBase64(buffer);
                this.ws.send(JSON.stringify({
                  audio_bytes: base64Audio
                }));
              }
            });
          }
        };
        this.mediaRecorder.start(250); // capture audio in 250ms chunks
        this.isStreaming = true;
      } catch (err) {
        console.error("Error accessing microphone:", err);
      }
    }
  
    stop() {
      if (this.mediaRecorder && this.isStreaming) {
        this.mediaRecorder.stop();
        this.mediaStream?.getTracks().forEach((track) => track.stop());
        this.isStreaming = false;
      }
    }
  }
  