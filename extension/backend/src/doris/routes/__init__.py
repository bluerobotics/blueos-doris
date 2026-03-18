"""API routes for DORIS backend."""

from .attitude import register_attitude_routes
from .blueos import register_blueos_routes
from .configurations import register_configuration_routes
from .dive import register_dive_routes
from .media import register_media_routes
from .missions import register_mission_routes
from .network import register_network_routes
from .sensors import register_sensor_routes
from .system import register_system_routes

__all__ = [
    "register_attitude_routes",
    "register_blueos_routes",
    "register_system_routes",
    "register_network_routes",
    "register_sensor_routes",
    "register_mission_routes",
    "register_media_routes",
    "register_configuration_routes",
    "register_dive_routes",
]

