import React, { useState } from "react";
import { defaultSettings, updateSettings } from "../../utils/settings";

const previousConversations = [
    { id: "conv1", title: "Chat from Jan 1" },
    { id: "conv2", title: "Chat from Feb 5" },
];

const UserInfo: React.FC = () => {
    const [name, setName] = useState(defaultSettings.userName);
    const [job, setJob] = useState(defaultSettings.userJob);
    const [selectedConversation, setSelectedConversation] = useState<string | null>(defaultSettings.selectedConversation);

    return (
        <div className="mt-4 bg-gray-600 p-3 rounded-lg">
        <h3 className="text-sm font-medium">User Information</h3>

        <label className="block text-sm font-medium mt-3">Name:</label>
        <input
            type="text"
            className="w-full mt-1 p-2 bg-gray-700 border border-gray-500 rounded-md"
            value={name}
            onChange={(e) => {
            setName(e.target.value);
            updateSettings("userName", e.target.value);
            }}
            placeholder="Enter user name"
        />

        <label className="block text-sm font-medium mt-3">Job:</label>
        <input
            type="text"
            className="w-full mt-1 p-2 bg-gray-700 border border-gray-500 rounded-md"
            value={job}
            onChange={(e) => {
            setJob(e.target.value);
            updateSettings("userJob", e.target.value);
            }}
            placeholder="Enter job title"
        />

        <label className="block text-sm font-medium mt-3">Previous Conversations:</label>
        <select
            className="w-full mt-1 p-2 bg-gray-700 border border-gray-500 rounded-md"
            value={selectedConversation || ""}
            onChange={(e) => {
            setSelectedConversation(e.target.value);
            updateSettings("selectedConversation", e.target.value);
            }}
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

export default UserInfo;
