"""BlueOS WiFi Manager v1.0 API client.

v1.0 endpoints (port 9000, prefix /v1.0):
  GET  /status              - Connection status
  GET  /scan                - Scan for available networks
  GET  /saved               - List saved networks
  POST /connect             - Connect to a network (body: {ssid, password}, query: ?hidden=bool)
  POST /remove              - Remove saved network (query: ?ssid=str)
  GET  /disconnect           - Disconnect from current network
  GET  /hotspot              - Get hotspot state
  POST /hotspot              - Toggle hotspot (query: ?enable=bool)
  GET  /hotspot_extended_status - Extended hotspot status
  GET  /smart_hotspot        - Check smart-hotspot state
  POST /smart_hotspot        - Toggle smart-hotspot (query: ?enable=bool)
  GET  /hotspot_credentials  - Get hotspot credentials
  POST /hotspot_credentials  - Set hotspot credentials (body: {ssid, password})
"""

from __future__ import annotations

from typing import Any

from ...base import BlueOSClient


class NetworkV1Client:
    """Client for BlueOS WiFi Manager v1.0 API."""

    API_VERSION = "v1.0"

    def __init__(self, base_url: str, timeout: float = 10.0):
        self._client = BlueOSClient(base_url, timeout=timeout)

    def _path(self, endpoint: str) -> str:
        return f"/{self.API_VERSION}{endpoint}"

    async def get_status(self) -> dict[str, Any]:
        """Get current connection status."""
        return await self._client.get(self._path("/status"))

    async def scan(self) -> list[dict[str, Any]]:
        """Scan for available WiFi networks.

        Returns list of ScannedWifiNetwork:
          {ssid, bssid, flags, frequency, signallevel}
        """
        return await self._client.get(self._path("/scan"))

    async def get_saved(self) -> list[dict[str, Any]]:
        """Get saved WiFi networks.

        Returns list of SavedWifiNetwork:
          {networkid, ssid, bssid?, flags?, nm_id?, nm_uuid?}
        """
        return await self._client.get(self._path("/saved"))

    async def connect(self, ssid: str, password: str, *, hidden: bool = False) -> Any:
        """Connect to a WiFi network."""
        return await self._client.post(
            self._path(f"/connect?hidden={str(hidden).lower()}"),
            json={"ssid": ssid, "password": password},
        )

    async def remove(self, ssid: str) -> Any:
        """Remove a saved WiFi network."""
        return await self._client.post(
            self._path("/remove"),
            data=None,
            json=None,
        )

    async def disconnect(self) -> Any:
        """Disconnect from current WiFi network.

        Note: v1 uses GET for disconnect.
        """
        return await self._client.get(self._path("/disconnect"))

    async def get_hotspot(self) -> dict[str, Any]:
        """Get hotspot state. Returns {supported, enabled}."""
        return await self._client.get(self._path("/hotspot"))

    async def set_hotspot(self, enable: bool) -> Any:
        """Enable or disable hotspot."""
        return await self._client.post(
            self._path(f"/hotspot?enable={str(enable).lower()}"),
        )

    async def get_hotspot_extended_status(self) -> dict[str, Any]:
        """Get extended hotspot status."""
        return await self._client.get(self._path("/hotspot_extended_status"))

    async def get_smart_hotspot(self) -> bool:
        """Check if smart-hotspot is enabled."""
        return await self._client.get(self._path("/smart_hotspot"))

    async def set_smart_hotspot(self, enable: bool) -> Any:
        """Enable or disable smart-hotspot."""
        return await self._client.post(
            self._path(f"/smart_hotspot?enable={str(enable).lower()}"),
        )

    async def get_hotspot_credentials(self) -> dict[str, Any]:
        """Get hotspot credentials. Returns {ssid, password}."""
        return await self._client.get(self._path("/hotspot_credentials"))

    async def set_hotspot_credentials(self, ssid: str, password: str) -> Any:
        """Set hotspot credentials."""
        return await self._client.post(
            self._path("/hotspot_credentials"),
            json={"ssid": ssid, "password": password},
        )

    async def close(self) -> None:
        await self._client.close()
