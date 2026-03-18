"""Dive control service.

Sets the DORIS_START MAVLink parameter via mavlink2rest to trigger
the onboard Lua dive script.

Uses the mavlink2rest helper endpoint to get a PARAM_SET template,
fills in the parameter name and value, and POSTs it. For reading,
sends a PARAM_REQUEST_READ then reads the cached PARAM_VALUE message.
"""

import asyncio
import json
import logging

import httpx

from ..config import blueos_services

logger = logging.getLogger(__name__)

PARAM_NAME = "DORIS_START"


def _mavlink2rest_url() -> str:
    return blueos_services.mavlink2rest


class DiveService:
    def __init__(self) -> None:
        self._client: httpx.AsyncClient | None = None
        self._last_known_value: float = 0.0

    @property
    def client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(timeout=10.0, follow_redirects=True)
        return self._client

    async def start_dive(self) -> bool:
        """Set DORIS_START=1 via PARAM_SET to trigger the Lua script."""
        ok = await self._set_param(PARAM_NAME, 1.0)
        if ok:
            self._last_known_value = 1.0
        return ok

    async def stop_dive(self) -> bool:
        """Set DORIS_START=0 via PARAM_SET to abort/reset."""
        ok = await self._set_param(PARAM_NAME, 0.0)
        if ok:
            self._last_known_value = 0.0
        return ok

    async def get_status(self) -> dict:
        """Read the current value of DORIS_START.

        Sends PARAM_REQUEST_READ then reads the PARAM_VALUE message cache.
        """
        base = _mavlink2rest_url()
        try:
            await self._request_param(PARAM_NAME)
            await asyncio.sleep(0.3)

            resp = await self.client.get(
                f"{base}/mavlink/vehicles/1/components/1/messages/PARAM_VALUE"
            )
            resp.raise_for_status()
            data = resp.json()
            message = data.get("message", {})
            param_id = "".join(
                c for c in message.get("param_id", []) if c != "\x00"
            )
            if param_id == PARAM_NAME:
                value = message.get("param_value", 0.0)
                self._last_known_value = value
                return {"param": PARAM_NAME, "value": value, "active": value >= 1.0}

            return {
                "param": PARAM_NAME,
                "value": self._last_known_value,
                "active": self._last_known_value >= 1.0,
            }
        except Exception as e:
            logger.warning(f"Could not read {PARAM_NAME}: {e}")
            return {
                "param": PARAM_NAME,
                "value": self._last_known_value,
                "active": self._last_known_value >= 1.0,
            }

    async def _request_param(self, name: str) -> None:
        """Send PARAM_REQUEST_READ so the autopilot emits a fresh PARAM_VALUE."""
        base = _mavlink2rest_url()
        payload = {
            "header": {"system_id": 255, "component_id": 0, "sequence": 0},
            "message": {
                "type": "PARAM_REQUEST_READ",
                "target_system": 1,
                "target_component": 1,
                "param_id": list(name.ljust(16, "\x00")),
                "param_index": -1,
            },
        }
        try:
            resp = await self.client.post(f"{base}/mavlink", json=payload)
            resp.raise_for_status()
        except Exception as e:
            logger.debug(f"PARAM_REQUEST_READ for {name} failed: {e}")

    async def _set_param(self, name: str, value: float) -> bool:
        """Send a PARAM_SET message via mavlink2rest."""
        base = _mavlink2rest_url()
        payload = {
            "header": {"system_id": 255, "component_id": 0, "sequence": 0},
            "message": {
                "type": "PARAM_SET",
                "target_system": 1,
                "target_component": 1,
                "param_id": list(name.ljust(16, "\x00")),
                "param_value": value,
                "param_type": {"type": "MAV_PARAM_TYPE_REAL32"},
            },
        }
        try:
            resp = await self.client.post(f"{base}/mavlink", json=payload)
            resp.raise_for_status()
            logger.info(f"Set {name}={value} (status {resp.status_code})")
            return True
        except Exception as e:
            logger.error(f"Failed to set {name}={value}: {e}")
            return False

    async def close(self) -> None:
        if self._client is not None and not self._client.is_closed:
            await self._client.aclose()
            self._client = None
