import React, { useState } from "react";
import { defaultSettings, updateSettings } from "../../utils/settings";

const voices = ["Alloy", "Nova", "Shimmer"];

const VoiceSelector: React.FC = () => {
    const [selectedVoice, setSelectedVoice] = useState(defaultSettings.voice);

    const handleVoiceChange = (voice: string) => {
        setSelectedVoice(voice);
        updateSettings("voice", voice);
    };

    return (
        <div className="mb-3">
        <label className="block text-sm font-medium">Select Voice:</label>
        <select
            className="mt-1 p-2 w-full bg-gray-600 border border-gray-500 rounded-md"
            value={selectedVoice}
            onChange={(e) => handleVoiceChange(e.target.value)}
        >
            {voices.map((voice) => (
            <option key={voice} value={voice}>
                {voice}
            </option>
            ))}
        </select>
        </div>
    );
};

export default VoiceSelector;
