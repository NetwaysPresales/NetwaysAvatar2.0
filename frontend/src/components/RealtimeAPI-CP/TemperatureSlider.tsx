import React, { useState } from "react";

const models = [
  { value: "gpt-4o-realtime-preview", label: "GPT-4o (Realtime)" },
  { value: "gpt-3.5-turbo", label: "GPT-3.5 Turbo" },
];

const ModelSelection: React.FC = () => {
  const [model, setModel] = useState<string>("gpt-4o-realtime-preview");

  return (
    <div className="mb-3">
      <label className="block text-sm font-medium">Select Model:</label>
      <select
        className="mt-1 p-2 w-full bg-gray-600 border border-gray-500 rounded-md"
        value={model}
        onChange={(e) => setModel(e.target.value)}
      >
        {models.map((m) => (
          <option key={m.value} value={m.value}>
            {m.label}
          </option>
        ))}
      </select>
    </div>
  );
};

export default ModelSelection;
