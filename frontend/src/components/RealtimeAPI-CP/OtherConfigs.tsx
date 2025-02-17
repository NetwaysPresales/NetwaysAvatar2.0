import React, { useState } from "react";
import { defaultSettings, updateSettings } from "../../utils/settings";

const OtherConfigs: React.FC = () => {
    const [temperature, setTemperature] = useState(defaultSettings.temperature);
    const [maxTokens, setMaxTokens] = useState(defaultSettings.maxTokens);
    const [useStreaming, setUseStreaming] = useState(defaultSettings.enableStreaming);

    return (
        <div className="mt-4 bg-gray-600 p-3 rounded-lg">
        <h3 className="text-sm font-medium">Other Configurations</h3>

        <div className="mt-3">
            <label className="block text-sm font-medium">Temperature:</label>
            <input
            type="range"
            min="0.1"
            max="1.0"
            step="0.1"
            value={temperature}
            onChange={(e) => {
                setTemperature(parseFloat(e.target.value));
                updateSettings("temperature", parseFloat(e.target.value));
            }}
            className="w-full mt-1"
            />
        </div>

        <div className="mt-3">
            <label className="block text-sm font-medium">Max Tokens:</label>
            <input
            type="number"
            className="w-full mt-1 p-2 bg-gray-700 border border-gray-500 rounded-md"
            value={maxTokens}
            onChange={(e) => {
                setMaxTokens(parseInt(e.target.value));
                updateSettings("maxTokens", parseInt(e.target.value));
            }}
            />
        </div>

        <div className="flex items-center mt-3">
            <input
            type="checkbox"
            checked={useStreaming}
            onChange={() => {
                setUseStreaming(!useStreaming);
                updateSettings("enableStreaming", !useStreaming);
            }}
            className="mr-2"
            />
            <span className="text-sm">Enable Streaming Responses</span>
        </div>
        </div>
    );
};

export default OtherConfigs;
