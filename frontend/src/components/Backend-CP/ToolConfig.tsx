import React, { useState, useEffect } from "react";
import { defaultSettings, updateSettings } from "../../utils/settings";
import { fetchAvailableTools } from "../../utils/api"; // API function

const ToolConfig: React.FC = () => {
  const [availableTools, setAvailableTools] = useState<{ id: string; name: string }[]>([]);
  const [selectedTools, setSelectedTools] = useState<string[]>(defaultSettings.enabledTools);

  useEffect(() => {
    fetchAvailableTools().then((tools) => {
      setAvailableTools(tools || []);
    });
  }, []);

  const toggleTool = (toolId: string) => {
    const newTools = selectedTools.includes(toolId)
      ? selectedTools.filter((t) => t !== toolId)
      : [...selectedTools, toolId];

    setSelectedTools(newTools);
    updateSettings("enabledTools", newTools);
  };

  return (
    <div className="mt-4 bg-gray-600 p-3 rounded-lg">
      <h3 className="text-sm font-medium">Tool Configuration</h3>
      <p className="text-xs text-gray-300 mb-2">Enable/disable tool calls for AI.</p>

      {availableTools.length > 0 ? (
        availableTools.map((tool) => (
          <div key={tool.id} className="flex items-center mt-2">
            <input
              type="checkbox"
              checked={selectedTools.includes(tool.id)}
              onChange={() => toggleTool(tool.id)}
              className="mr-2"
            />
            <span className="text-sm">{tool.name}</span>
          </div>
        ))
      ) : (
        <p className="text-xs text-gray-300">Fetching available tools...</p>
      )}
    </div>
  );
};

export default ToolConfig;
