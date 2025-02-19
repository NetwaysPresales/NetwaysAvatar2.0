import React, { useCallback } from "react";
import { ISettings } from "../models/settingsModel";

interface VADSettingsProps {
  settings: ISettings;
  setSettings: React.Dispatch<React.SetStateAction<ISettings>>;
}

const VADSettings: React.FC<VADSettingsProps> = ({ settings, setSettings }) => {
  const { vad } = settings;

  const handleThresholdChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const newThreshold = parseFloat(e.target.value);
    setSettings((prev: ISettings) => ({
      ...prev,
      vad: { ...prev.vad, vad_threshold: newThreshold },
    }));
  }, [setSettings]);

  const handlePaddingChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const newPadding = parseInt(e.target.value, 10);
    setSettings((prev: ISettings) => ({
      ...prev,
      vad: { ...prev.vad, vad_prefix_padding: newPadding },
    }));
  }, [setSettings]);

  const handleSilenceDurationChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const newSilence = parseInt(e.target.value, 10);
    setSettings((prev: ISettings) => ({
      ...prev,
      vad: { ...prev.vad, vad_silence_duration: newSilence },
    }));
  }, [setSettings]);

  const handleCreateResponseChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    setSettings((prev: ISettings) => ({
      ...prev,
      vad: { ...prev.vad, vad_create_response: e.target.checked },
    }));
  }, [setSettings]);

  return (
    <div className="bg-gray-600 p-3 rounded-lg mb-4">
      <h3 className="text-sm font-medium">Voice Activity Detection (VAD) Settings</h3>
      
      <label className="block text-sm font-medium mt-3">VAD Threshold:</label>
      <input
        type="range"
        min="0.0"
        max="1.0"
        step="0.1"
        value={vad.vad_threshold}
        onChange={handleThresholdChange}
        className="w-full mt-1"
      />
      
      <label className="block text-sm font-medium mt-3">Prefix Padding (ms):</label>
      <input
        type="number"
        value={vad.vad_prefix_padding}
        onChange={handlePaddingChange}
        className="w-full mt-1 p-2 bg-gray-700 rounded-md"
      />
      
      <label className="block text-sm font-medium mt-3">Silence Duration (ms):</label>
      <input
        type="number"
        value={vad.vad_silence_duration}
        onChange={handleSilenceDurationChange}
        className="w-full mt-1 p-2 bg-gray-700 rounded-md"
      />
      
      <div className="flex items-center mt-3">
        <input
          type="checkbox"
          checked={vad.vad_create_response}
          onChange={handleCreateResponseChange}
          className="mr-2"
        />
        <span className="text-sm">Create Response Automatically</span>
      </div>
    </div>
  );
};

export default VADSettings;
