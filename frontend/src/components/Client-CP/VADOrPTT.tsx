import React, { useState } from "react";

const VADOrPTT: React.FC = () => {
    const [mode, setMode] = useState<string>("ptt");

    return (
        <div className="mb-3">
        <label className="block text-sm font-medium">Select Input Mode:</label>
        <select
            className="mt-1 p-2 w-full bg-gray-600 border border-gray-500 rounded-md"
            value={mode}
            onChange={(e) => setMode(e.target.value)}
        >
            <option value="ptt">Push-to-Talk</option>
            <option value="vad">Voice Activity Detection (VAD)</option>
        </select>
        </div>
    );
};

export default VADOrPTT;
