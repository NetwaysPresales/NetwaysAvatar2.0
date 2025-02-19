export class AudioPlayer {
  private audioContext: AudioContext;
  private isPlaying: boolean = false;
  private queue: ArrayBuffer[] = [];

  constructor() {
    this.audioContext = new AudioContext();
  }

  // Modified enqueue to accept either an ArrayBuffer or a base64 string.
  enqueue(data: ArrayBuffer | string) {
    let buffer: ArrayBuffer;
    if (typeof data === "string") {
      // If data is a string, assume it's base64-encoded PCM16 audio.
      const decodedBuffer = this.base64ToArrayBuffer(data);
      // Wrap raw PCM16 data in a WAV header (adjust sampleRate/channels as needed)
      buffer = this.pcm16ToWav(decodedBuffer, 16000, 1);
    } else {
      buffer = data;
    }
    this.queue.push(buffer);
    if (!this.isPlaying) {
      this.playQueue();
    }
  }

  async playQueue() {
    this.isPlaying = true;
    while (this.queue.length > 0) {
      const buffer = this.queue.shift();
      if (buffer) {
        try {
          const audioBuffer = await this.audioContext.decodeAudioData(buffer.slice(0));
          const source = this.audioContext.createBufferSource();
          source.buffer = audioBuffer;
          source.connect(this.audioContext.destination);
          source.start(0);
          await new Promise<void>((resolve) => {
            source.onended = () => resolve();
          });
        } catch (err) {
          console.error("Error playing audio chunk:", err);
        }
      }
    }
    this.isPlaying = false;
  }

  stop() {
    // Clear the queue and suspend the context.
    this.queue = [];
    if (this.audioContext.state === "running") {
      this.audioContext.suspend();
    }
  }

  resume() {
    if (this.audioContext.state !== "running") {
      this.audioContext.resume();
    }
  }

  // Helper function to decode a base64 string into an ArrayBuffer.
  private base64ToArrayBuffer(base64: string): ArrayBuffer {
    const binaryString = atob(base64);
    const len = binaryString.length;
    const bytes = new Uint8Array(len);
    for (let i = 0; i < len; i++) {
      bytes[i] = binaryString.charCodeAt(i);
    }
    return bytes.buffer;
  }

  // Helper function to wrap raw PCM16 data in a WAV container.
  private pcm16ToWav(pcmData: ArrayBuffer, sampleRate = 16000, channels = 1): ArrayBuffer {
    const headerSize = 44;
    const pcmBytes = new Uint8Array(pcmData);
    const wavBuffer = new ArrayBuffer(headerSize + pcmBytes.length);
    const view = new DataView(wavBuffer);

    // RIFF identifier 'RIFF'
    this.writeString(view, 0, "RIFF");
    // File length minus first 8 bytes
    view.setUint32(4, 36 + pcmBytes.length, true);
    // RIFF type 'WAVE'
    this.writeString(view, 8, "WAVE");
    // Format chunk identifier 'fmt '
    this.writeString(view, 12, "fmt ");
    // Format chunk length
    view.setUint32(16, 16, true);
    // Audio format (1 = PCM)
    view.setUint16(20, 1, true);
    // Number of channels
    view.setUint16(22, channels, true);
    // Sample rate
    view.setUint32(24, sampleRate, true);
    // Byte rate (sampleRate * channels * bytes per sample)
    view.setUint32(28, sampleRate * channels * 2, true);
    // Block align (channels * bytes per sample)
    view.setUint16(32, channels * 2, true);
    // Bits per sample
    view.setUint16(34, 16, true);
    // Data chunk identifier 'data'
    this.writeString(view, 36, "data");
    // Data chunk length
    view.setUint32(40, pcmBytes.length, true);

    // Write PCM data after header
    new Uint8Array(wavBuffer, headerSize).set(pcmBytes);
    return wavBuffer;
  }

  private writeString(view: DataView, offset: number, str: string) {
    for (let i = 0; i < str.length; i++) {
      view.setUint8(offset + i, str.charCodeAt(i));
    }
  }
}
