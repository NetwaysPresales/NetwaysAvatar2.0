import React, { useState } from "react";
import { defaultSettings, updateSettings } from "../../utils/settings";

const FaceRecognitionToggle: React.FC = () => {
    const [enabled, setEnabled] = useState(defaultSettings.faceRecognition);

    return (
        <div className="flex items-center justify-between mb-3">
        <span className="text-sm font-medium">Enable Face Recognition:</span>
        <button
            className={`px-4 py-2 rounded-md ${
            enabled ? "bg-green-600" : "bg-gray-500"
            }`}
            onClick={() => {
            setEnabled(!enabled);
            updateSettings("faceRecognition", !enabled);
            }}
        >
            {enabled ? "Enabled" : "Disabled"}
        </button>
        </div>
    );
};

export default FaceRecognitionToggle;
