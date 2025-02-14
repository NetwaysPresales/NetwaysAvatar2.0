import { useWebSocket } from "../hooks/useWebSocket";

export default function StatusLog() {
    const { messages } = useWebSocket("ws://localhost:8000/realtime");

    return (
        <div className="p-6 bg-white shadow-md rounded-lg max-w-md mx-auto mt-6">
            <h2 className="text-lg font-semibold text-gray-800 mb-3">Live Logs</h2>
            <ul className="list-disc list-inside bg-gray-100 p-3 rounded-lg">
                {messages.map((msg, index) => (
                    <li key={index} className="text-sm text-gray-700">{msg}</li>
                ))}
            </ul>
        </div>
    );
}
