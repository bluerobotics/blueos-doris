"""Barometer and thermometer detection service.

Detects connected barometer and thermometer by listening for
SCALED_PRESSURE2 MAVLink messages via the mavlink2rest WebSocket.
If a message arrives within the timeout, the sensors are present.

Fields used from SCALED_PRESSURE2:
  - press_abs (hPa): absolute pressure  -> Barometer
  - temperature (cdegC): temperature     -> Thermometer
"""

import asyncio
import json
import logging

import websockets

from ..config import blueos_services
from ..models.sensors import ModuleInfo

logger = logging.getLogger(__name__)

WS_TIMEOUT = 3.0


def _ws_url() -> str:
    """Build the WebSocket URL filtered to SCALED_PRESSURE2."""
    base = blueos_services.mavlink2rest
    ws_base = base.replace("http://", "ws://").replace("https://", "wss://")
    return f"{ws_base}/ws/mavlink?filter=SCALED_PRESSURE2"


def _parse_message(raw: str) -> dict | None:
    """Parse a SCALED_PRESSURE2 WebSocket message."""
    if not raw.startswith("{"):
        return None
    try:
        data = json.loads(raw)
        msg = data.get("message", {})
        if msg.get("type") == "SCALED_PRESSURE2":
            return msg
        return None
    except (json.JSONDecodeError, TypeError):
        return None


class BarometerService:
    """Detects barometer/thermometer via SCALED_PRESSURE2 messages."""

    async def get_modules(self) -> list[ModuleInfo]:
        """Return ModuleInfo entries for barometer and thermometer if detected."""
        msg = await self._receive_pressure()
        if msg is None:
            return []

        modules: list[ModuleInfo] = []

        press_abs = msg.get("press_abs")
        if press_abs is not None:
            modules.append(
                ModuleInfo(
                    id="barometer",
                    name="Barometer",
                    type="sensor",
                    status="connected",
                    module_status=f"Ready: {press_abs:.1f} hPa",
                )
            )

        temp_cdeg = msg.get("temperature")
        if temp_cdeg is not None:
            temp_c = temp_cdeg / 100.0
            modules.append(
                ModuleInfo(
                    id="thermometer",
                    name="Thermometer",
                    type="sensor",
                    status="connected",
                    module_status=f"Ready: {temp_c:.1f} °C",
                )
            )

        return modules

    async def _receive_pressure(self) -> dict | None:
        """Connect to the WebSocket and wait for one SCALED_PRESSURE2 message."""
        try:
            async with websockets.connect(_ws_url(), close_timeout=2) as ws:
                try:
                    async with asyncio.timeout(WS_TIMEOUT):
                        while True:
                            raw = await ws.recv()
                            parsed = _parse_message(raw)
                            if parsed is not None:
                                return parsed
                except TimeoutError:
                    logger.debug("No SCALED_PRESSURE2 received within timeout")
        except Exception as e:
            logger.warning(f"Failed to detect barometer/thermometer: {e}")
        return None

    async def close(self) -> None:
        """No persistent resources to close."""
