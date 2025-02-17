import React, { useState } from "react";

const ServerVADSettings: React.FC = () => {
  const [threshold, setThreshold] = useState<number>(0.5);
  const [padding, setPadding] = useState<number>(300);
  const [silenceDuration, setSilenceDuration] = useState<number>(200);
  const [createResponse, setCreateResponse] = useState<boolean>(true);

  return (
    <div className="mt-3 p-3 bg-gray-600 rounded-lg">
        <label className="block text-sm font-medium">VAD Threshold:</label>
        <input
            type="range"
            min="0.1"
            max="1.0"
            step="0.1"
            value={threshold}
            onChange={(e) => setThreshold(parseFloat(e.target.value))}
            className="w-full mt-1"
        />

        <label className="block text-sm font-medium mt-3">Prefix Padding (ms):</label>
        <input
            type="number"
            className="w-full mt-1 p-2 bg-gray-700 rounded-md"
            value={padding}
            onChange={(e) => setPadding(parseInt(e.target.value))}
        />

        <label className="block text-sm font-medium mt-3">Silence Duration (ms):</label>
        <input
            type="number"
            className="w-full mt-1 p-2 bg-gray-700 rounded-md"
            value={silenceDuration}
            onChange={(e) => setSilenceDuration(parseInt(e.target.value))}
        />

        <div className="flex items-center mt-3">
            <input
            type="checkbox"
            checked={createResponse}
            onChange={() => setCreateResponse(!createResponse)}
            className="mr-2"
            />
            <span className="text-sm">Create Response</span>
        </div>
    </div>
  );
};

export default ServerVADSettings;
