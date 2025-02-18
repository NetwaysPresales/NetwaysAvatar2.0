import asyncio
from fastapi import Response
from starlette.responses import StreamingResponse

class SSEManager:
    """Manages SSE connections for real-time event streaming."""

    def __init__(self):
        self.clients = set()  # Store active SSE connections

    async def register(self, response: Response):
        """
        Registers a new SSE connection.
        :param response: FastAPI Response object for streaming
        """
        self.clients.add(response)
        try:
            while True:
                await asyncio.sleep(1)  # Keep the connection alive
        except asyncio.CancelledError:
            self.clients.remove(response)

    def send_event(self, data: dict):
        """
        Sends an event to all connected SSE clients.
        :param data: Dictionary representing event payload
        """
        for client in self.clients:
            try:
                client.body += f"data: {data}\n\n".encode("utf-8")
            except Exception:
                self.clients.remove(client)

sse_manager = SSEManager()
