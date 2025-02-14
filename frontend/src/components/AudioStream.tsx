import { useState, useRef } from "react";
import { useWebSocket } from "../hooks/useWebSocket";

export default function AudioStream() {
    const { sendMessage } = useWebSocket("ws://localhost:8000/realtime");
    const [recording, setRecording] = useState(false);
    const [mode, setMode] = useState("vad"); // "vad" or "ptt"
    const mediaRecorderRef = useRef<MediaRecorder | null>(null);

    const startRecording = async () => {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorderRef.current = new MediaRecorder(stream);
        mediaRecorderRef.current.start();

        mediaRecorderRef.current.ondataavailable = async (event) => {
            const audioBlob = event.data;
            const arrayBuffer = await audioBlob.arrayBuffer();
            sendMessage(arrayBuffer);
        };

        setRecording(true);
    };

    const stopRecording = () => {
        mediaRecorderRef.current?.stop();
        setRecording(false);
    };

    return (
        <div className="p-4 bg-gray-700 rounded-lg">
            <h2 className="text-lg font-semibold">Audio Streaming</h2>

            {/* Mode Selector */}
            <div className="mt-2">
                <label className="block text-gray-300">Mode:</label>
                <select
                    value={mode}
                    onChange={(e) => setMode(e.target.value)}
                    className="w-full p-2 bg-gray-800 text-white rounded-lg border-gray-600"
                >
                    <option value="vad">Server VAD</option>
                    <option value="ptt">Push to Talk</option>
                </select>
            </div>

            {/* Push-to-Talk Button */}
            {mode === "ptt" ? (
                <button
                    onMouseDown={startRecording}
                    onMouseUp={stopRecording}
                    className="mt-4 w-full py-2 bg-blue-500 hover:bg-blue-600 rounded-lg"
                >
                    Hold to Talk
                </button>
            ) : (
                <button
                    onClick={recording ? stopRecording : startRecording}
                    className={`mt-4 w-full py-2 rounded-lg ${recording ? "bg-red-500 hover:bg-red-600" : "bg-gray-500 hover:bg-gray-600"}`}
                >
                    {recording ? "Stop Recording" : "Start Recording"}
                </button>
            )}
        </div>
    );
}
