// ChatUI.tsx
import React, { useState, useEffect, useRef } from "react";
import { ISettings } from "../models/settingsModel";
import { AudioPlayer } from "../utils/audioPlayer";
import { MicStreamer } from "../utils/micStreamer";

interface ChatUIProps {
  settings: ISettings;
  convoWs: WebSocket;
}

const ChatUI: React.FC<ChatUIProps> = ({ settings, convoWs }) => {
  // Chat log for transcript messages.
  const [messages, setMessages] = useState<string[]>([]);
  // micEnabled controls whether audio capture is sent.
  const [micEnabled, setMicEnabled] = useState<boolean>(true);

  // Instantiate AudioPlayer to sequentially play received audio chunks.
  const audioPlayerRef = useRef<AudioPlayer | null>(null);
  // Instantiate MicStreamer to capture microphone audio.
  const micStreamerRef = useRef<MicStreamer | null>(null);

  // Setup AudioPlayer instance.
  useEffect(() => {
    audioPlayerRef.current = new AudioPlayer();
    return () => {
      audioPlayerRef.current?.stop();
    };
  }, []);

  // Wrap the global conversation WebSocket to attach our onMessage handler.
  useEffect(() => {
    if (!convoWs) return;

    const handleMessage = (event: MessageEvent) => {
      try {
        const msg = JSON.parse(event.data);
        // For transcript events, assume payload has "delta" or "transcript".
        if (msg.type === "response.audio_transcript.delta") {
          setMessages((prev) => [...prev, msg.delta || msg.transcript || JSON.stringify(msg)]);
        } else if(msg.type === "response.audio.delta") {
          audioPlayerRef.current?.enqueue(msg.delta)
        } else {
          setMessages((prev) => [...prev, JSON.stringify(msg)]);
        }
      } catch (err) {
        console.error("Error parsing conversation message:", err);
        setMessages((prev) => [...prev, event.data]);
      }
    };

    convoWs.addEventListener("message", handleMessage);
    return () => {
      convoWs.removeEventListener("message", handleMessage);
    };
  }, [convoWs]);

  // Setup microphone streaming using MicStreamer, wrapping the global convoWs.
  useEffect(() => {
    if (micEnabled && convoWs) {
      micStreamerRef.current = new MicStreamer(convoWs, () => micEnabled);
      micStreamerRef.current.start();
    } else {
      micStreamerRef.current?.stop();
      micStreamerRef.current = null;
    }
    return () => {
      micStreamerRef.current?.stop();
      micStreamerRef.current = null;
    };
  }, [micEnabled, convoWs]);

  const toggleMic = () => {
    setMicEnabled((prev) => !prev);
    console.log("Microphone", micEnabled ? "disabled" : "enabled");
  };

  return (
    <div className="p-4">
      <div className="mb-4">
        <button 
          className="px-4 py-2 bg-blue-500 text-white rounded" 
          onClick={toggleMic}
        >
          {micEnabled ? "Disable Microphone" : "Enable Microphone"}
        </button>
      </div>
      <div className="mb-4">
        <strong>Input Mode:</strong> {settings.app.input_mode}
      </div>
      <div className="border p-4 h-64 overflow-y-auto bg-gray-100">
        {messages.map((msg, idx) => (
          <div key={idx} className="mb-2">
            {msg}
          </div>
        ))}
      </div>
    </div>
  );
};

export default ChatUI;
