import React, { useState, useEffect } from "react";
import { defaultSettings, Settings } from "../utils/settings";
import { IoMenu, IoClose } from "react-icons/io5";
import OpenAISettings from "./OpenAISettings";
import VADSettings from "./VADSettings";
import UserSettings from "./UserSettings";
import AppSettings from "./AppSettings";
import { sendSettingsToBackend, listenForSettingsUpdate } from "../utils/api";

const ControlPanel: React.FC = () => {
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const [settings, setSettings] = useState<Settings>(defaultSettings);

  // Listen for backend settings updates (full overwrite)
  useEffect(() => {
    listenForSettingsUpdate((newSettings: Settings) => {
      setSettings(newSettings);
    });
  }, []);

  const handleStartConversation = () => {
    console.log("Conversation started");
    setSettings((prev) => ({
      ...prev,
      app: { ...prev.app, is_conversation_active: true },
    }));
  };

  const handleEndConversation = () => {
    console.log("Conversation ended");
    setSettings((prev) => ({
      ...prev,
      app: { ...prev.app, is_conversation_active: false },
    }));
  };

  const handleSaveSettings = async () => {
    await sendSettingsToBackend(settings);
    console.log("Settings saved to backend:", settings);
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

        {/* Scrollable Content */}
        <div className="flex-1 overflow-y-auto p-5 space-y-4">
          <OpenAISettings settings={settings} setSettings={setSettings} />
          <VADSettings settings={settings} setSettings={setSettings} />
          <UserSettings settings={settings} setSettings={setSettings} />
          <AppSettings settings={settings} setSettings={setSettings} />
          <div className="flex gap-2">
            <button
              className={`w-1/2 bg-[#10a37f] hover:bg-[#0e8d6b] text-white px-4 py-2 rounded-md`}
              onClick={handleStartConversation}
              disabled={settings.app.is_conversation_active}
            >
              Start Conversation
            </button>
            <button
              className={`w-1/2 bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-md`}
              onClick={handleEndConversation}
              disabled={!settings.app.is_conversation_active}
            >
              End Conversation
            </button>
          </div>
        </div>

        {/* Footer: Save Settings */}
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
