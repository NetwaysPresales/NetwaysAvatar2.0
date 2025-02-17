import React, { useEffect } from "react";
import ControlPanel from "./components/ControlPanel";

const App: React.FC = () => {
    useEffect(() => {
        const requestPermissions = async () => {
            try {
                // Request both microphone and camera permissions
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true, video: true });
                console.log("Microphone and camera permissions granted.");
                // Optionally, you can store the stream or use it in your app.
            } catch (error) {
                console.error("Error requesting permissions:", error);
                // Optionally, handle the error, such as showing a message to the user.
            }
        };
    
        requestPermissions();
    }, []);

    return (
        <div className="min-h-screen bg-[#202123] text-white">
        <ControlPanel />
        <div className="flex justify-center items-center h-screen">
            <h1 className="text-4xl font-bold text-[#ececf1]">AI Chat Interface</h1>
        </div>
        </div>
    );
};

export default App;
