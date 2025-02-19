export const createConvoSocket = (url: string): WebSocket => {
	const ws = new WebSocket(url);

	ws.onopen = () => {
		console.log("Convo WebSocket connected:", url);
	};

	ws.onerror = (e) => {
		console.error("Convo WebSocket error:", e);
	};

	ws.onclose = (e) => {
		console.log("Convo WebSocket closed:", e);
	};

	return ws;
};

export const sendConvoMessage = (message: object): void => {
	if (window.convoWs && window.convoWs.readyState === WebSocket.OPEN) {
		window.convoWs.send(JSON.stringify(message));
	} else {
		console.error("Convo WS is not connected.");
	}
};
