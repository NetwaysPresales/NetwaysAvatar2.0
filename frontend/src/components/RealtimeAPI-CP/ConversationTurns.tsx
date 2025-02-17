import React, { useState } from "react";
import { defaultSettings, updateSettings } from "../../utils/settings";
import ServerVADSettings from "./ServerVADSettings";

const ConversationTurns: React.FC = () => {
    const [mode, setMode] = useState(defaultSettings.serverVAD ? "vad" : "ptt");

    const handleModeChange = (value: string) => {
        setMode(value);
        updateSettings("serverVAD", value === "vad");
    };

    return (
        <div className="mb-3">
        <label className="block text-sm font-medium">Conversation Turn Mode:</label>
        <select
            className="mt-1 p-2 w-full bg-gray-600 border border-gray-500 rounded-md"
            value={mode}
            onChange={(e) => handleModeChange(e.target.value)}
        >
            <option value="ptt">Push-to-Talk</option>
            <option value="vad">Server VAD</option>
        </select>

        {mode === "vad" && <ServerVADSettings />}
        </div>
    );
};

export default ConversationTurns;
