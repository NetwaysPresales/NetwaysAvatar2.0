import React, { useState, useCallback } from "react";
import { ISettings } from "../models/settingsModel";

const previousConversations = [
  { id: "conv1", title: "Chat from Jan 1" },
  { id: "conv2", title: "Chat from Feb 5" },
];

interface UserSettingsProps {
  settings: ISettings;
  setSettings: React.Dispatch<React.SetStateAction<ISettings>>;
}

const UserSettings: React.FC<UserSettingsProps> = ({ settings, setSettings }) => {
  const [name, setName] = useState<string>(settings.user.user_name || "");
  const [job, setJob] = useState<string>(settings.user.user_job || "");
  const [selectedConversation, setSelectedConversation] = useState<string | null>(
    settings.user.selected_conversation || null
  );

  const handleNameChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const newName = e.target.value;
      setName(newName);
      setSettings((prev: ISettings) => ({
        ...prev,
        user: { ...prev.user, user_name: newName },
      }));
    },
    [setSettings]
  );

  const handleJobChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const newJob = e.target.value;
      setJob(newJob);
      setSettings((prev: ISettings) => ({
        ...prev,
        user: { ...prev.user, user_job: newJob },
      }));
    },
    [setSettings]
  );

  const handleConversationChange = useCallback(
    (e: React.ChangeEvent<HTMLSelectElement>) => {
      const convId = e.target.value;
      setSelectedConversation(convId);
      setSettings((prev: ISettings) => ({
        ...prev,
        user: { ...prev.user, selected_conversation: convId },
      }));
    },
    [setSettings]
  );

  return (
    <div className="bg-gray-600 p-3 rounded-lg mb-4">
      <h3 className="text-sm font-medium">User Information</h3>
      
      <label className="block text-sm font-medium mt-3">Name:</label>
      <input
        type="text"
        value={name}
        onChange={handleNameChange}
        className="w-full mt-1 p-2 bg-gray-700 rounded-md"
        placeholder="Enter user name"
      />
      
      <label className="block text-sm font-medium mt-3">Job:</label>
      <input
        type="text"
        value={job}
        onChange={handleJobChange}
        className="w-full mt-1 p-2 bg-gray-700 rounded-md"
        placeholder="Enter job title"
      />
      
      <label className="block text-sm font-medium mt-3">Previous Conversations:</label>
      <select
        value={selectedConversation || ""}
        onChange={handleConversationChange}
        className="w-full mt-1 p-2 bg-gray-700 rounded-md"
      >
        <option value="">Select a conversation</option>
        {previousConversations.map((conv) => (
          <option key={conv.id} value={conv.id}>
            {conv.title}
          </option>
        ))}
      </select>
    </div>
  );
};

export default UserSettings;
