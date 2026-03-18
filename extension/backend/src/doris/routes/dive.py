"""Dive control routes.

Exposes endpoints to start/stop dives by setting the DORIS_START
MAVLink parameter, and to query current dive status.
"""

import json
import logging

from robyn import Robyn

from ..services.dive import DiveService

logger = logging.getLogger(__name__)

dive_service = DiveService()


def register_dive_routes(app: Robyn) -> None:
    @app.post("/api/v1/dive/start")
    async def start_dive():
        ok = await dive_service.start_dive()
        return json.dumps({"success": ok, "message": "DORIS_START set to 1" if ok else "Failed to set parameter"})

    @app.post("/api/v1/dive/stop")
    async def stop_dive():
        ok = await dive_service.stop_dive()
        return json.dumps({"success": ok, "message": "DORIS_START set to 0" if ok else "Failed to set parameter"})

    @app.get("/api/v1/dive/status")
    async def dive_status():
        status = await dive_service.get_status()
        return json.dumps(status)
