"""WebSocket route for streaming vehicle attitude data.

Connects to mavlink2rest ATTITUDE WebSocket and forwards parsed
attitude updates to connected frontend clients in real-time.

Uses Robyn's WebSocket class with on("connect"/"message"/"close")
callback pattern and asyncio background tasks for push delivery.
"""

import asyncio
import json
import logging

import websockets

from robyn import Robyn, WebSocket

from ..services.attitude import mavlink2rest_attitude_ws_url, parse_attitude_message

logger = logging.getLogger(__name__)

RECONNECT_DELAY = 2.0
MAX_RETRIES = 10


def register_attitude_routes(app: Robyn) -> None:
    """Register the attitude WebSocket endpoint."""

    attitude_ws = WebSocket(app, "/ws/attitude")
    active_clients: dict[str, asyncio.Task] = {}

    @attitude_ws.on("connect")
    async def on_connect(ws):
        client_id = ws.id
        logger.info(f"Attitude WebSocket client connected: {client_id}")

        async def push_attitude():
            ws_url = mavlink2rest_attitude_ws_url()
            retries = 0
            while retries < MAX_RETRIES:
                try:
                    async with websockets.connect(ws_url, close_timeout=2) as mav_ws:
                        retries = 0
                        while True:
                            raw = await mav_ws.recv()
                            payload = parse_attitude_message(raw)
                            if payload:
                                await ws.async_send_to(client_id, json.dumps(payload))
                except websockets.exceptions.ConnectionClosed:
                    retries += 1
                    await asyncio.sleep(RECONNECT_DELAY)
                except ConnectionRefusedError:
                    retries += 1
                    try:
                        await ws.async_send_to(client_id, json.dumps({
                            "type": "status",
                            "message": f"MAVLink2Rest unavailable, retry {retries}/{MAX_RETRIES}",
                        }))
                    except Exception:
                        return
                    await asyncio.sleep(RECONNECT_DELAY)
                except asyncio.CancelledError:
                    return
                except Exception as e:
                    logger.warning(f"Attitude push error for {client_id}: {e}")
                    return

        task = asyncio.create_task(push_attitude())
        active_clients[client_id] = task
        return json.dumps({"type": "connected", "message": "Attitude stream ready"})

    @attitude_ws.on("message")
    async def on_message(ws, msg):
        return ""

    @attitude_ws.on("close")
    async def on_close(ws):
        client_id = ws.id
        task = active_clients.pop(client_id, None)
        if task and not task.done():
            task.cancel()
        logger.info(f"Attitude WebSocket client disconnected: {client_id}")
        return ""
