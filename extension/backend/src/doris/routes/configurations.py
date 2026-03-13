"""Configuration API routes."""

import json
from urllib.parse import unquote

from robyn import Response, Robyn

from ..models.configuration import DeploymentConfiguration
from ..services.storage import StorageService


def register_configuration_routes(app: Robyn) -> None:
    """Register configuration CRUD API routes."""

    storage_service = StorageService()

    @app.get("/api/v1/configurations")
    async def list_configurations(request):
        """List all saved configurations."""
        try:
            configs = await storage_service.list_configurations()
            return json.dumps([c.model_dump(mode="json") for c in configs])
        except Exception as e:
            return Response(
                status_code=500,
                description=json.dumps({"error": str(e)}),
                headers={"Content-Type": "application/json"},
            )

    @app.get("/api/v1/configurations/:name")
    async def get_configuration(request):
        """Load a configuration by name."""
        try:
            name = unquote(request.path_params.get("name", ""))
            if not name:
                return Response(
                    status_code=400,
                    description=json.dumps({"error": "Missing configuration name"}),
                    headers={"Content-Type": "application/json"},
                )

            config = await storage_service.load_configuration(name)
            if config is None:
                return Response(
                    status_code=404,
                    description=json.dumps({"error": f"Configuration '{name}' not found"}),
                    headers={"Content-Type": "application/json"},
                )

            return config.model_dump_json()
        except Exception as e:
            return Response(
                status_code=500,
                description=json.dumps({"error": str(e)}),
                headers={"Content-Type": "application/json"},
            )

    @app.post("/api/v1/configurations")
    async def save_configuration(request):
        """Save a new or overwrite an existing configuration."""
        try:
            data = json.loads(request.body)
            config = DeploymentConfiguration.model_validate(data)
            saved = await storage_service.save_configuration(config)
            return saved.model_dump_json()
        except json.JSONDecodeError:
            return Response(
                status_code=400,
                description=json.dumps({"error": "Invalid JSON"}),
                headers={"Content-Type": "application/json"},
            )
        except Exception as e:
            return Response(
                status_code=400,
                description=json.dumps({"error": str(e)}),
                headers={"Content-Type": "application/json"},
            )

    @app.delete("/api/v1/configurations/:name")
    async def delete_configuration(request):
        """Delete a configuration by name."""
        try:
            name = unquote(request.path_params.get("name", ""))
            if not name:
                return Response(
                    status_code=400,
                    description=json.dumps({"error": "Missing configuration name"}),
                    headers={"Content-Type": "application/json"},
                )

            deleted = await storage_service.delete_configuration(name)
            if not deleted:
                return Response(
                    status_code=404,
                    description=json.dumps({"error": f"Configuration '{name}' not found"}),
                    headers={"Content-Type": "application/json"},
                )

            return json.dumps({"success": True})
        except Exception as e:
            return Response(
                status_code=500,
                description=json.dumps({"error": str(e)}),
                headers={"Content-Type": "application/json"},
            )
