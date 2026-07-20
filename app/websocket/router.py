from __future__ import annotations

import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.core.logger import logger
from app.websocket.manager import manager

router = APIRouter(tags=["WebSocket"])


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await manager.connect(websocket)

    logger.info(
        "WebSocket conectado (%s conexões)",
        manager.total_connections,
    )

    try:
        while True:

            data = await websocket.receive_text()

            try:
                payload = json.loads(data)
            except Exception:
                payload = {}

            if payload.get("type") == "ping":
                await manager.send(
                    websocket,
                    {"type": "pong"},
                )

    except WebSocketDisconnect:

        await manager.disconnect(websocket)

        logger.info(
            "WebSocket desconectado (%s conexões)",
            manager.total_connections,
        )

    except Exception as exc:

        logger.exception(exc)

        await manager.disconnect(websocket)
