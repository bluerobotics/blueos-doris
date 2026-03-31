"""Dive control routes.

Exposes endpoints to start/stop dives by setting the DORIS_START
MAVLink parameter, and to query current dive status.

When starting a dive with a configuration name, the route loads
the configuration from storage and pushes DORIS_* params before
triggering.
"""

import json
import logging

from robyn import Robyn

from ..services.dive import DiveService
from ..services.storage import StorageService

logger = logging.getLogger(__name__)

dive_service = DiveService()
storage_service = StorageService()


def register_dive_routes(app: Robyn) -> None:
    @app.post("/api/v1/dive/start")
    async def start_dive(request):
        config = None
        try:
            body = json.loads(request.body) if request.body else {}
        except (json.JSONDecodeError, TypeError):
            body = {}

        config_name = body.get("configuration")
        if config_name:
            config = await storage_service.load_configuration(config_name)
            if config is None:
                return json.dumps({
                    "success": False,
                    "message": f"Configuration '{config_name}' not found",
                })
            logger.info(f"Starting dive with configuration: {config_name}")

        ok = await dive_service.start_dive(config=config)
        msg = "DORIS_START set to 1"
        if config_name:
            msg += f" (config: {config_name})"
        return json.dumps({"success": ok, "message": msg if ok else "Failed to set parameter"})

    @app.post("/api/v1/dive/stop")
    async def stop_dive():
        ok = await dive_service.stop_dive()
        return json.dumps({"success": ok, "message": "DORIS_START set to 0" if ok else "Failed to set parameter"})

    @app.get("/api/v1/dive/status")
    async def dive_status():
        status = await dive_service.get_status()
        return json.dumps(status)
