"""Notification routes.

Provides REST endpoints for listing, reading, deleting notifications
and managing notification settings.  The GET /notifications endpoint
also triggers a system-event poll so new notifications are generated
in real time without a separate background task.
"""

import json
import logging

from robyn import Robyn

from ..models.notifications import NotificationSettings
from ..services.dive import DiveService
from ..services.notifications import NotificationService
from ..services.system import SystemService

logger = logging.getLogger(__name__)

notification_service = NotificationService()
system_service = SystemService()
dive_service = DiveService()


async def _poll_events() -> None:
    """Gather live system data and feed it to the notification service."""
    battery_level: float | None = None
    battery_voltage: float | None = None
    storage_used: float | None = None
    storage_avail: float | None = None
    net_connected: bool | None = None
    net_ssid: str | None = None
    dive_active: bool | None = None

    try:
        battery = await system_service.get_battery_info()
        battery_level = battery.level
        battery_voltage = battery.voltage
    except Exception:
        pass

    try:
        storage = await system_service.get_storage_info()
        storage_used = storage.used_percent
        storage_avail = storage.available_gb
    except Exception:
        pass

    try:
        from ..services.network import NetworkService
        net_svc = NetworkService()
        status = await net_svc.get_status()
        net_connected = status.is_connected
        net_ssid = status.ssid
    except Exception:
        pass

    try:
        dive_status = await dive_service.get_status()
        dive_active = dive_status.get("active", False)
    except Exception:
        pass

    await notification_service.poll_system_events(
        battery_level=battery_level,
        battery_voltage=battery_voltage,
        storage_used_percent=storage_used,
        storage_available_gb=storage_avail,
        network_connected=net_connected,
        network_ssid=net_ssid,
        dive_active=dive_active,
    )


def register_notification_routes(app: Robyn) -> None:
    @app.get("/api/v1/notifications")
    async def list_notifications():
        await _poll_events()
        items = notification_service.list_notifications()
        return json.dumps(
            [n.model_dump(mode="json") for n in items],
            default=str,
        )

    @app.get("/api/v1/notifications/unread-count")
    async def unread_count():
        return json.dumps({"count": notification_service.unread_count()})

    @app.post("/api/v1/notifications/:id/read")
    async def mark_read(request):
        nid = request.path_params.get("id", "")
        ok = notification_service.mark_read(nid)
        return json.dumps({"success": ok})

    @app.post("/api/v1/notifications/read-all")
    async def mark_all_read():
        notification_service.mark_all_read()
        return json.dumps({"success": True})

    @app.delete("/api/v1/notifications/:id")
    async def delete_notification(request):
        nid = request.path_params.get("id", "")
        ok = notification_service.delete_notification(nid)
        return json.dumps({"success": ok})

    @app.get("/api/v1/notifications/settings")
    async def get_settings():
        return notification_service.get_settings().model_dump_json()

    @app.put("/api/v1/notifications/settings")
    async def update_settings(request):
        try:
            body = json.loads(request.body) if request.body else {}
        except (json.JSONDecodeError, TypeError):
            return json.dumps({"error": "Invalid JSON"})
        settings = NotificationSettings.model_validate(body)
        updated = notification_service.update_settings(settings)
        return updated.model_dump_json()
