import { API_ENDPOINTS } from "../config";
import { Settings } from "./settings";

export const sendSettingsToBackend = async (settings: Settings): Promise<void> => {
  try {
    const response = await fetch(API_ENDPOINTS.updateSettings, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(settings),
    });

    if (!response.ok) {
      throw new Error("Failed to update settings.");
    }
  } catch (error) {
    console.error("Error saving settings:", error);
  }
};

export const listenForSettingsUpdate = (
  callback: (newSettings: Settings) => void
): void => {
  const eventSource = new EventSource(API_ENDPOINTS.pushSettings);

  eventSource.onmessage = (event) => {
    const newSettings = JSON.parse(event.data) as Settings;
    console.log("Received updated settings from backend:", newSettings);
    callback(newSettings);
  };

  eventSource.onerror = (error) => {
    console.error("Error listening for settings updates:", error);
  };
};

