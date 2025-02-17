export const fetchUserInfo = async () => {
    try {
        const response = await fetch("/api/user-info");
        if (!response.ok) throw new Error("Failed to fetch user info.");
        return await response.json();
    } catch (error) {
        console.error("Error fetching user info:", error);
        return null;
    }
};
    
export const fetchConversationSummary = async (conversationId: string) => {
    try {
        const response = await fetch(`/api/conversation-summary/${conversationId}`);
        if (!response.ok) throw new Error("Failed to fetch conversation summary.");
        const data = await response.json();
        return data.summary;
    } catch (error) {
        console.error("Error fetching conversation summary:", error);
        return null;
    }
};

export const fetchAvailableTools = async () => {
    try {
        const response = await fetch("/api/available-tools");
        if (!response.ok) throw new Error("Failed to fetch available tools.");
        return await response.json();
    } catch (error) {
        console.error("Error fetching available tools:", error);
        return [];
    }
};

export const sendSettingsToBackend = async (settings: any) => {
    try {
        const response = await fetch("/api/update-settings", {
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

export const listenForSettingsUpdate = (callback: (newSettings: any) => void) => {
    const eventSource = new EventSource("/api/push-settings");
  
    eventSource.onmessage = (event) => {
        const newSettings = JSON.parse(event.data);
        console.log("Received updated settings from backend:", newSettings);
        callback(newSettings);
    };
  
    eventSource.onerror = (error) => {
        console.error("Error listening for settings updates:", error);
    };
};