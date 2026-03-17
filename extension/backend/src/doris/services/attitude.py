"""Attitude data service.

Streams vehicle attitude (roll, pitch, yaw) from mavlink2rest
WebSocket using the ATTITUDE MAVLink message filter.

ATTITUDE message fields (from MAVLink spec):
  - time_boot_ms: Timestamp (ms since boot)
  - roll:  Roll angle in radians (-pi..+pi)
  - pitch: Pitch angle in radians (-pi..+pi)
  - yaw:   Yaw angle in radians (-pi..+pi)
  - rollspeed:  Roll angular speed (rad/s)
  - pitchspeed: Pitch angular speed (rad/s)
  - yawspeed:   Yaw angular speed (rad/s)
"""

import json
import logging
import math
from datetime import datetime, timezone

from ..config import blueos_services

logger = logging.getLogger(__name__)


def mavlink2rest_attitude_ws_url() -> str:
    """Build the WebSocket URL filtered to ATTITUDE messages."""
    base = blueos_services.mavlink2rest
    ws_base = base.replace("http://", "ws://").replace("https://", "wss://")
    return f"{ws_base}/ws/mavlink?filter=ATTITUDE"


def parse_attitude_message(raw: str) -> dict | None:
    """Parse an ATTITUDE WebSocket message into a structured payload.

    Returns a dict with attitude data or None if the message is invalid.
    """
    if not raw.startswith("{"):
        return None
    try:
        data = json.loads(raw)
        msg = data.get("message", {})
        if msg.get("type") != "ATTITUDE":
            return None

        roll = msg.get("roll", 0.0)
        pitch = msg.get("pitch", 0.0)
        yaw = msg.get("yaw", 0.0)

        return {
            "type": "attitude_update",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "time_boot_ms": msg.get("time_boot_ms", 0),
            "attitude": {
                "roll_rad": round(roll, 4),
                "pitch_rad": round(pitch, 4),
                "yaw_rad": round(yaw, 4),
                "roll_deg": round(math.degrees(roll), 2),
                "pitch_deg": round(math.degrees(pitch), 2),
                "yaw_deg": round(math.degrees(yaw), 2),
            },
            "rates": {
                "rollspeed": round(msg.get("rollspeed", 0.0), 4),
                "pitchspeed": round(msg.get("pitchspeed", 0.0), 4),
                "yawspeed": round(msg.get("yawspeed", 0.0), 4),
            },
        }
    except (json.JSONDecodeError, TypeError):
        return None
