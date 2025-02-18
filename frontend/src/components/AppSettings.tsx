import React from "react";
import { Settings } from "../utils/settings";

interface AppSettingsProps {
  settings: Settings;
  setSettings: React.Dispatch<React.SetStateAction<Settings>>;
}

const AppSettings: React.FC<AppSettingsProps> = ({ settings, setSettings }) => {
  const { app } = settings;

  const handleInputModeChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSettings((prev) => ({
      ...prev,
      app: { ...prev.app, input_mode: e.target.value },
    }));
  };

  const handleInstructionPromptChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setSettings((prev) => ({
      ...prev,
      app: { ...prev.app, instruction_prompt: e.target.value },
    }));
  };

  const handleMetahumanToggle = () => {
    setSettings((prev) => ({
      ...prev,
      app: { ...prev.app, metahuman_sync: !prev.app.metahuman_sync },
    }));
  };

  const handleFaceRecognitionToggle = () => {
    setSettings((prev) => ({
      ...prev,
      app: { ...prev.app, face_recognition: !prev.app.face_recognition },
    }));
  };

  return (
    <div className="bg-gray-600 p-3 rounded-lg mb-4">
      <h3 className="text-sm font-medium">Application Settings</h3>
      
      <label className="block text-sm font-medium mt-3">Input Mode:</label>
      <select
        className="mt-1 p-2 w-full bg-gray-700 rounded-md"
        value={app.input_mode}
        onChange={handleInputModeChange}
      >
        <option value="ptt">Push-to-Talk</option>
        <option value="server_vad">Server VAD</option>
      </select>
      
      <label className="block text-sm font-medium mt-3">Instruction Prompt:</label>
      <textarea
        className="mt-1 p-2 w-full bg-gray-700 rounded-md"
        value={app.instruction_prompt}
        onChange={handleInstructionPromptChange}
      />
      
      <div className="flex items-center mt-3">
        <button
          className={`px-4 py-2 rounded-md ${app.metahuman_sync ? "bg-green-600" : "bg-gray-500"}`}
          onClick={handleMetahumanToggle}
        >
          {app.metahuman_sync ? "Metahuman Enabled" : "Metahuman Disabled"}
        </button>
      </div>
      
      <div className="flex items-center mt-3">
        <button
          className={`px-4 py-2 rounded-md ${app.face_recognition ? "bg-green-600" : "bg-gray-500"}`}
          onClick={handleFaceRecognitionToggle}
        >
          {app.face_recognition ? "Face Recognition Enabled" : "Face Recognition Disabled"}
        </button>
      </div>
    </div>
  );
};

export default AppSettings;
