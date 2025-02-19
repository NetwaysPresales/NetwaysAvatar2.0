// App.tsx
import React from "react";
import ControlPanel from "./components/ControlPanel";
import ChatUI from "./components/ChatUI";
import { useDataSync } from "./ws/dataSyncSocket";
import { defaultSettings } from "./models/settingsModel";
import { defaultState } from "./models/stateModel";
import * as config from "./config"
import { createConvoSocket } from "./ws/convoSocket";

const App: React.FC = () => {
    // useDataSync hook initializes the WS connection and returns settings, state and their setters.
    const { settings, setSettings, state, setState } = useDataSync(defaultSettings, defaultState, config.WS_DATA_SYNC_URL);
    const convoWs = createConvoSocket(config.WS_CONVO_URL)

    return (
        <div>
        <ControlPanel settings={settings} setSettings={setSettings} state={state} setState={setState} />
        <ChatUI settings={settings} convoWs={convoWs} />
        </div>
    );
};

export default App;
