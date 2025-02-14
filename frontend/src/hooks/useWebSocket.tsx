import { useEffect, useState } from "react";

export function useWebSocket(url: string) {
    const [socket, setSocket] = useState<WebSocket | null>(null);
    const [messages, setMessages] = useState<string[]>([]);
    const [isConnected, setIsConnected] = useState(false);

    useEffect(() => {
        const ws = new WebSocket(url);
        ws.binaryType = "arraybuffer"; // Enable binary data

        ws.onopen = () => {
            setIsConnected(true);
            console.log("WebSocket Connected!");
        };

        ws.onmessage = (event) => {
            if (typeof event.data === "string") {
                setMessages((prev) => [...prev, event.data]);
            } else if (event.data instanceof ArrayBuffer) {
                console.log("Received binary data:", event.data);
            }
        };

        ws.onclose = () => {
            setIsConnected(false);
            console.log("WebSocket Disconnected!");
        };

        setSocket(ws);

        return () => ws.close();
    }, [url]);

    const sendMessage = (message: string | ArrayBuffer) => {
        if (socket && isConnected) {
            socket.send(message);
        }
    };

    return { isConnected, messages, sendMessage };
}
