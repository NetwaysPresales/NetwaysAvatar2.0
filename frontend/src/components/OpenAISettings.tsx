import React, { useCallback } from "react";
import { ISettings } from "../models/settingsModel"; // Adjust the import path as needed

interface OpenAISettingsProps {
  settings: ISettings;
  setSettings: React.Dispatch<React.SetStateAction<ISettings>>;
}

const models = [
  { value: "gpt-4o-realtime-preview", label: "GPT-4o (Realtime)" },
  { value: "gpt-3.5-turbo", label: "GPT-3.5 Turbo" },
];

const voices = ["Alloy", "Nova", "Shimmer"];

const OpenAISettings: React.FC<OpenAISettingsProps> = ({ settings, setSettings }) => {
  const { openai } = settings;

  const handleModelChange = useCallback((e: React.ChangeEvent<HTMLSelectElement>) => {
    setSettings((prev: ISettings) => ({
      ...prev,
      openai: { ...prev.openai, model: e.target.value },
    }));
  }, [setSettings]);

  const handleVoiceChange = useCallback((e: React.ChangeEvent<HTMLSelectElement>) => {
    setSettings((prev: ISettings) => ({
      ...prev,
      openai: { ...prev.openai, voice: e.target.value },
    }));
  }, [setSettings]);

  const handleTemperatureChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const newTemp = parseFloat(e.target.value);
    setSettings((prev: ISettings) => ({
      ...prev,
      openai: { ...prev.openai, temperature: newTemp },
    }));
  }, [setSettings]);

  const handleMaxTokensChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const newMax = parseInt(e.target.value, 10);
    setSettings((prev: ISettings) => ({
      ...prev,
      openai: { ...prev.openai, max_tokens: newMax },
    }));
  }, [setSettings]);

  const handleEnableStreamingChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    setSettings((prev: ISettings) => ({
      ...prev,
      openai: { ...prev.openai, enable_streaming: e.target.checked },
    }));
  }, [setSettings]);

  return (
    <div className="bg-gray-600 p-3 rounded-lg mb-4">
      <h3 className="text-sm font-medium">OpenAI Configuration</h3>
      
      <label className="block text-sm font-medium mt-3">Select Model:</label>
      <select
        className="mt-1 p-2 w-full bg-gray-700 rounded-md"
        value={openai.model}
        onChange={handleModelChange}
      >
        {models.map((m) => (
          <option key={m.value} value={m.value}>
            {m.label}
          </option>
        ))}
      </select>
      
      <label className="block text-sm font-medium mt-3">Select Voice:</label>
      <select
        className="mt-1 p-2 w-full bg-gray-700 rounded-md"
        value={openai.voice}
        onChange={handleVoiceChange}
      >
        {voices.map((voice) => (
          <option key={voice} value={voice}>
            {voice}
          </option>
        ))}
      </select>
      
      <label className="block text-sm font-medium mt-3">Temperature:</label>
      <input
        type="range"
        min="0.1"
        max="1.0"
        step="0.1"
        value={openai.temperature}
        onChange={handleTemperatureChange}
        className="w-full mt-1"
      />
      
      <label className="block text-sm font-medium mt-3">Max Tokens:</label>
      <input
        type="number"
        value={openai.max_tokens}
        onChange={handleMaxTokensChange}
        className="w-full mt-1 p-2 bg-gray-700 rounded-md"
      />
      
      <div className="flex items-center mt-3">
        <input
          type="checkbox"
          checked={openai.enable_streaming}
          onChange={handleEnableStreamingChange}
          className="mr-2"
        />
        <span className="text-sm">Enable Streaming Responses</span>
      </div>
    </div>
  );
};

export default OpenAISettings;
