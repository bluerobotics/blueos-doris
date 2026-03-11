"""BlueOS WiFi Manager network client abstraction (v1 + v2)."""

from .client import NetworkClient
from .v1 import NetworkV1Client
from .v2 import NetworkV2Client

__all__ = ["NetworkClient", "NetworkV1Client", "NetworkV2Client"]
