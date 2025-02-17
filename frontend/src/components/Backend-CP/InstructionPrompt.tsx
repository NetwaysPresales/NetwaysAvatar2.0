import React, { useState } from "react";
import { defaultSettings, updateSettings } from "../../utils/settings";

const InstructionPrompt: React.FC = () => {
    const [prompt, setPrompt] = useState(defaultSettings.instructionPrompt);

    return (
        <div className="mb-3">
        <label className="block text-sm font-medium">Instruction Prompt:</label>
        <textarea
            className="mt-1 p-2 w-full bg-gray-600 border border-gray-500 rounded-md"
            value={prompt}
            onChange={(e) => {
            setPrompt(e.target.value);
            updateSettings("instructionPrompt", e.target.value);
            }}
        />
        </div>
    );
};

export default InstructionPrompt;
