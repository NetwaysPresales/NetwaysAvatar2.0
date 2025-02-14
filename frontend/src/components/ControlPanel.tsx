import { useState } from "react";
import { useWebSocket } from "../hooks/useWebSocket";

export default function ControlPanel() {
    const { isConnected, sendMessage } = useWebSocket("ws://localhost:8000/realtime");
    const [voice, setVoice] = useState("alloy");
    const [neuroSyncEnabled, setNeuroSyncEnabled] = useState(false);

    const handleStart = () => sendMessage(JSON.stringify({ event: "START" }));
    const handleEnd = () => sendMessage(JSON.stringify({ event: "END" }));
    const updateSettings = () => sendMessage(JSON.stringify({ event: "CONFIG", voice, neuroSyncEnabled }));

    return (
        <div className="p-6 text-white">
            <h2 className="text-xl font-bold mb-4">AI Agent Control Panel</h2>
            <p className={`mb-4 ${isConnected ? "text-green-400" : "text-red-400"}`}>
                Status: {isConnected ? "Connected" : "Disconnected"}
            </p>

            {/* Session Controls */}
            <div className="flex space-x-4">
                <button 
                    onClick={handleStart} 
                    className="bg-gray-700 text-white font-semibold py-2 px-4 rounded-lg transition-all duration-300 transform hover:scale-105 hover:bg-gray-600"
                >
                    Start Session
                </button>
                <button 
                    onClick={handleEnd} 
                    className="bg-gray-700 text-white font-semibold py-2 px-4 rounded-lg transition-all duration-300 transform hover:scale-105 hover:bg-gray-600"
                >
                    End Session
                </button>
            </div>

            {/* Voice Model Selector */}
            <div className="mt-4">
                <label className="block font-semibold">Voice Model:</label>
                <select 
                    value={voice} 
                    onChange={(e) => setVoice(e.target.value)}
                    className="w-full border border-gray-600 bg-gray-700 text-white p-2 rounded-lg hover:border-gray-400 transition-all duration-300 transform hover:scale-105"
                >
                    <option value="alloy">Alloy</option>
                    <option value="echo">Echo</option>
                </select>
            </div>

            {/* NeuroSync Toggle */}
            <div className="mt-2 flex items-center">
                <label className="font-semibold mr-2">NeuroSync:</label>
                <input 
                    type="checkbox" 
                    checked={neuroSyncEnabled} 
                    onChange={() => setNeuroSyncEnabled(!neuroSyncEnabled)}
                    className="w-5 h-5 bg-gray-700 border-gray-500 rounded cursor-pointer hover:border-gray-400 transition-all duration-300 transform hover:scale-110"
                />
            </div>

            {/* Update Config Button */}
            <button 
                onClick={updateSettings} 
                className="mt-4 bg-gray-700 text-white font-semibold py-2 px-4 rounded-lg transition-all duration-300 transform hover:scale-105 hover:bg-gray-600 w-full"
            >
                Update Config
            </button>
        </div>
    );
}
