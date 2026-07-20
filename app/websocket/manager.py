from __future__ import annotations

import asyncio
from typing import List

from fastapi import WebSocket


class WebSocketManager:

    def __init__(self):
        self.connections: List[WebSocket] = []
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        async with self._lock:
            if websocket not in self.connections:
                self.connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        async with self._lock:
            if websocket in self.connections:
                self.connections.remove(websocket)

    async def send(self, websocket: WebSocket, message: dict):
        try:
            await websocket.send_json(message)
        except Exception:
            await self.disconnect(websocket)

    async def broadcast(self, message: dict):
        for ws in list(self.connections):
            try:
                await ws.send_json(message)
            except Exception:
                await self.disconnect(ws)

    @property
    def total_connections(self):
        return len(self.connections)


manager = WebSocketManager()
