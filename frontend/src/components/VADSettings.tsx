import React from "react";
import { Settings } from "../utils/settings";

interface VADSettingsProps {
  settings: Settings;
  setSettings: React.Dispatch<React.SetStateAction<Settings>>;
}

const VADSettings: React.FC<VADSettingsProps> = ({ settings, setSettings }) => {
  const { vad } = settings;

  const handleThresholdChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSettings((prev) => ({
      ...prev,
      vad: { ...prev.vad, vadThreshold: parseFloat(e.target.value) },
    }));
  };

  const handlePaddingChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSettings((prev) => ({
      ...prev,
      vad: { ...prev.vad, vadPrefixPadding: parseInt(e.target.value, 10) },
    }));
  };

  const handleSilenceDurationChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSettings((prev) => ({
      ...prev,
      vad: { ...prev.vad, vadSilenceDuration: parseInt(e.target.value, 10) },
    }));
  };

  const handleCreateResponseChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSettings((prev) => ({
      ...prev,
      vad: { ...prev.vad, vadCreateResponse: e.target.checked },
    }));
  };

  return (
    <div className="bg-gray-600 p-3 rounded-lg mb-4">
      <h3 className="text-sm font-medium">Voice Activity Detection (VAD) Settings</h3>
      
      <label className="block text-sm font-medium mt-3">VAD Threshold:</label>
      <input
        type="range"
        min="0.0"
        max="1.0"
        step="0.1"
        value={vad.vadThreshold}
        onChange={handleThresholdChange}
        className="w-full mt-1"
      />
      
      <label className="block text-sm font-medium mt-3">Prefix Padding (ms):</label>
      <input
        type="number"
        value={vad.vadPrefixPadding}
        onChange={handlePaddingChange}
        className="w-full mt-1 p-2 bg-gray-700 rounded-md"
      />
      
      <label className="block text-sm font-medium mt-3">Silence Duration (ms):</label>
      <input
        type="number"
        value={vad.vadSilenceDuration}
        onChange={handleSilenceDurationChange}
        className="w-full mt-1 p-2 bg-gray-700 rounded-md"
      />
      
      <div className="flex items-center mt-3">
        <input
          type="checkbox"
          checked={vad.vadCreateResponse}
          onChange={handleCreateResponseChange}
          className="mr-2"
        />
        <span className="text-sm">Create Response Automatically</span>
      </div>
    </div>
  );
};

export default VADSettings;
