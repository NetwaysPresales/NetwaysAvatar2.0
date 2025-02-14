import Sidebar from "./components/Sidebar";
import { useState } from "react";
import { FiMaximize } from "react-icons/fi";

export default function App() {
    const [isFullScreen, setIsFullScreen] = useState(false);
    const [sidebarOpen, setSidebarOpen] = useState(true);

    const toggleFullScreen = () => {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen();
        } else if (document.exitFullscreen) {
            document.exitFullscreen();
        }
        setIsFullScreen(!isFullScreen);
    };

    return (
        <div className="flex bg-gray-800 text-white min-h-screen">
            <Sidebar isOpen={sidebarOpen} setIsOpen={setSidebarOpen} />

            {/* Main Content */}
            <main
                className={`transition-all duration-300 flex-1 flex flex-col items-center justify-center px-6 py-10 ${
                    sidebarOpen ? "ml-72" : "ml-0"
                }`}
            >
                <div className="bg-gray-700 shadow-md rounded-lg max-w-3xl w-full text-center p-6">
                    <h1 className="text-3xl font-bold">AI Agent Dashboard</h1>
                    <p className="text-gray-400 mt-2">Main content will go here...</p>
                </div>

                {/* Fullscreen Button */}
                <button
                    onClick={toggleFullScreen}
                    className="absolute top-4 right-4 bg-gray-700 p-2 rounded-md hover:bg-gray-600"
                >
                    <FiMaximize size={24} />
                </button>
            </main>
        </div>
    );
}
