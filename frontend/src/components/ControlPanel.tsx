import React, { useState, useEffect } from "react";
import { defaultSettings, updateSettings, getSettings, Settings } from "../utils/settings";
import { IoMenu, IoClose } from "react-icons/io5"; // Import icons
import ConversationTurns from "./RealtimeAPI-CP/ConversationTurns";
import VoiceSelector from "./RealtimeAPI-CP/VoiceSelector";
import OtherConfigs from "./RealtimeAPI-CP/OtherConfigs";
import InstructionPrompt from "./Backend-CP/InstructionPrompt";
import ToolConfig from "./Backend-CP/ToolConfig";
import UserInfo from "./Backend-CP/UserInfo";
import MetahumanToggle from "./Client-CP/MetahumanToggle";
import FaceRecognitionToggle from "./Client-CP/FaceRecognitionToggle";
import { sendSettingsToBackend, listenForSettingsUpdate } from "../utils/api";

const ControlPanel: React.FC = () => {
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const [settings, setSettings] = useState<Settings>(defaultSettings);

  useEffect(() => {
    // Listen for updates from backend and apply them
    listenForSettingsUpdate((newSettings: Partial<Settings>) => {
      Object.entries(newSettings).forEach(([key, value]) => {
        if (value !== undefined) {
          const settingKey = key as keyof Settings;
          if (typeof defaultSettings[settingKey] === typeof value) {
            updateSettings(settingKey, value as Settings[keyof Settings]);
          }
        }
      });
      // Update local state to reflect changes.
      setSettings(getSettings());
    });
  }, []);

  const handleStartConversation = () => {
    console.log("Conversation started");
    updateSettings("isConversationActive", true);
    setSettings((prev) => ({ ...prev, isConversationActive: true }));
  };

  const handleEndConversation = () => {
    console.log("Conversation ended");
    updateSettings("isConversationActive", false);
    setSettings((prev) => ({ ...prev, isConversationActive: false }));
  };

  const handleSaveSettings = async () => {
    const currentSettings = getSettings();
    await sendSettingsToBackend(currentSettings);
    console.log("Settings saved to backend:", currentSettings);
  };

  return (
    <>
      {/* Hamburger Icon (only shown when panel is closed) */}
      {!isOpen && (
        <button
          className="fixed top-4 left-4 text-white bg-[#10a37f] p-2 rounded-md shadow-md z-50"
          onClick={() => setIsOpen(true)}
        >
          <IoMenu size={24} />
        </button>
      )}

      {/* Side Panel */}
      <div
        className={`fixed top-0 left-0 h-full bg-[#202123] text-[#ececf1] w-80 shadow-lg transition-transform flex flex-col ${
          isOpen ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        {/* Header */}
        <div className="flex justify-between items-center p-4 border-b border-gray-600">
          <h2 className="text-lg font-semibold">Ameera Settings</h2>
          <button onClick={() => setIsOpen(false)} className="text-white">
            <IoClose size={24} />
          </button>
        </div>

        {/* Scrollable Content Area */}
        <div className="flex-1 overflow-y-auto p-5">
          {/* Start/End Conversation Buttons */}
          <div className="mb-4">
            <button
              className={`w-full ${
                settings.isConversationActive
                  ? "bg-gray-500 cursor-not-allowed"
                  : "bg-[#10a37f] hover:bg-[#0e8d6b]"
              } text-white px-4 py-2 rounded-md mb-2`}
              onClick={handleStartConversation}
              disabled={settings.isConversationActive}
            >
              Start Conversation
            </button>
            <button
              className={`w-full ${
                !settings.isConversationActive
                  ? "bg-gray-500 cursor-not-allowed"
                  : "bg-red-500 hover:bg-red-600"
              } text-white px-4 py-2 rounded-md`}
              onClick={handleEndConversation}
              disabled={!settings.isConversationActive}
            >
              End Conversation
            </button>
          </div>

          {/* Realtime API Settings */}
          <div className="bg-[#343541] p-4 rounded-lg mb-4">
            <h3 className="text-lg font-semibold mb-2">Realtime API</h3>
            <ConversationTurns />
            <VoiceSelector />
            <OtherConfigs />
          </div>

          {/* Backend Settings */}
          <div className="bg-[#343541] p-4 rounded-lg mb-4">
            <h3 className="text-lg font-semibold mb-2">Backend Settings</h3>
            <InstructionPrompt />
            <ToolConfig />
            <UserInfo />
          </div>

          {/* Client Settings */}
          <div className="bg-[#343541] p-4 rounded-lg">
            <h3 className="text-lg font-semibold mb-2">Client Settings</h3>
            <MetahumanToggle />
            <FaceRecognitionToggle />
          </div>
        </div>

        {/* Footer: Save Button */}
        <div className="p-4 border-t border-gray-600">
          <button
            className="w-full bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-md"
            onClick={handleSaveSettings}
          >
            Save Settings
          </button>
        </div>
      </div>
    </>
  );
};

export default ControlPanel;
