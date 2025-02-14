import { FiMenu, FiX } from "react-icons/fi";
import ControlPanel from "./ControlPanel";
import AudioStream from "./AudioStream";
import StatusLog from "./StatusLog";

export default function Sidebar({ isOpen , setIsOpen }: { isOpen: boolean, setIsOpen: React.Dispatch<React.SetStateAction<boolean>> }) {
    return (
        <>
            {/* Sidebar - Fixed size, just slides in/out */}
            <div
                className={`fixed h-screen w-72 bg-gray-900 text-white shadow-md transition-transform duration-300 ${
                    isOpen ? "translate-x-0" : "-translate-x-full"
                }`}
            >
                <div className="flex flex-col h-full p-4">
                    {/* Sidebar Header */}
                    <div className="flex justify-between items-center mb-4">
                        <h2 className="text-xl font-semibold">Ameera AI</h2>
                        <button
                            onClick={() => setIsOpen(false)}
                            className="text-gray-400 hover:text-white transition-colors duration-200"
                        >
                            <FiX size={24} />
                        </button>
                    </div>

                    {/* Sidebar Content */}
                    <div className="space-y-6">
                        <ControlPanel />
                        <AudioStream />
                        <StatusLog />
                    </div>
                </div>
            </div>

            {/* Toggle Button - Slides in when sidebar is closed */}
            <button
                onClick={() => setIsOpen(true)}
                className={`fixed top-4 left-4 bg-gray-700 p-2 rounded-md text-white shadow-md transition-opacity duration-300 hover:bg-gray-600 ${
                    isOpen ? "opacity-0 pointer-events-none" : "opacity-100"
                }`}
            >
                <FiMenu size={24} />
            </button>
        </>
    );
}
