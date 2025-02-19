import { ISettings } from "../models/settingsModel";
import { IState } from "../models/stateModel";
import { DataSyncPayload } from "../models/dataPayloadModel";
import { useState, useEffect, useRef } from "react";

export const createDataSyncSocket = (
  url: string,
  onMessage: (data: DataSyncPayload) => void,
  onError?: (error: Event) => void,
  onClose?: (event: CloseEvent) => void
): WebSocket => {
  const ws: WebSocket = new WebSocket(url);

  ws.onopen = () => {
    	console.log("Data sync WebSocket connected");
  };

  ws.onmessage = (event: MessageEvent) => {
    try {
		const data: DataSyncPayload = JSON.parse(event.data);
		console.log("Received data sync message:", data);
		onMessage(data);
    } catch (error) {
      	console.error("Error parsing data sync message:", error);
    }
  };

  ws.onerror = (event: Event) => {
    console.error("Data sync WebSocket error:", event);
    if (onError) onError(event);
  };

  ws.onclose = (event: CloseEvent) => {
    console.log("Data sync WebSocket closed:", event);
    if (onClose) onClose(event);
  };

  return ws;
};

export function useDataSync(
  initialSettings: ISettings,
  initialState: IState,
  wsUrl: string
) {
  const [settings, setSettings] = useState<ISettings>(initialSettings);
  const [state, setState] = useState<IState>(initialState);
  const wsRef = useRef<WebSocket | null>(null);
  // Use refs to store the last sent values.
  const lastSentSettingsRef = useRef<ISettings>(initialSettings);
  const lastSentStateRef = useRef<IState>(initialState);

  useEffect(() => {
    wsRef.current = createDataSyncSocket(wsUrl, (data: DataSyncPayload) => {
      console.log("Received update from server:", data);
      // Update local state, but only if it’s different.
      if (data.settings && JSON.stringify(data.settings) !== JSON.stringify(settings)) {
        setSettings(data.settings);
      }
      if (data.state && JSON.stringify(data.state) !== JSON.stringify(state)) {
        setState(data.state);
      }
    });
    return () => {
      wsRef.current?.close();
    };
  }, [wsUrl, settings, state]);

  useEffect(() => {
    // Only send an update if settings have changed relative to the last sent value.
    if (
      wsRef.current &&
      wsRef.current.readyState === WebSocket.OPEN &&
      JSON.stringify(settings) !== JSON.stringify(lastSentSettingsRef.current)
    ) {
      const payload = { settings };
      wsRef.current.send(JSON.stringify(payload));
      console.log("Sent settings update via data sync WS:", payload);
      lastSentSettingsRef.current = settings;
    }
  }, [settings]);

  useEffect(() => {
    // Only send an update if state has changed relative to the last sent value.
    if (
      wsRef.current &&
      wsRef.current.readyState === WebSocket.OPEN &&
      JSON.stringify(state) !== JSON.stringify(lastSentStateRef.current)
    ) {
      const payload = { state };
      wsRef.current.send(JSON.stringify(payload));
      console.log("Sent state update via data sync WS:", payload);
      lastSentStateRef.current = state;
    }
  }, [state]);

  return { settings, setSettings, state, setState };
}