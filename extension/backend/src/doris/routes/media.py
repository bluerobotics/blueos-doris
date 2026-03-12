"""Media API routes."""

import json
import mimetypes
from urllib.parse import unquote

from robyn import Response, Robyn

from ..models.media import MediaType
from ..services.storage import StorageService


def register_media_routes(app: Robyn) -> None:
    """Register media-related API routes."""

    storage_service = StorageService()

    @app.get("/api/v1/media/files")
    async def get_media_files(request):
        """Get list of media files with optional filtering."""
        try:
            raw_mission_id = request.query_params.get("mission_id", None)
            mission_id = unquote(raw_mission_id) if raw_mission_id else None
            media_type_str = request.query_params.get("type", None)
            limit = int(request.query_params.get("limit", "50"))
            offset = int(request.query_params.get("offset", "0"))

            media_type = None
            if media_type_str:
                media_type = MediaType(media_type_str)

            files = await storage_service.get_media_files(
                mission_id=mission_id,
                media_type=media_type,
                limit=limit,
                offset=offset,
            )

            return json.dumps([f.model_dump(mode="json") for f in files])
        except Exception as e:
            return Response(
                status_code=500,
                description=json.dumps({"error": str(e)}),
                headers={"Content-Type": "application/json"},
            )

    @app.get("/api/v1/media/missions")
    async def get_missions_with_media(request):
        """Get list of missions that have media."""
        try:
            missions = await storage_service.get_missions_with_media()
            return json.dumps([m.model_dump(mode="json") for m in missions])
        except Exception as e:
            return Response(
                status_code=500,
                description=json.dumps({"error": str(e)}),
                headers={"Content-Type": "application/json"},
            )

    @app.get("/api/v1/media/download")
    async def download_file(request):
        """Download a file by its relative path (passed as ?path=...)."""
        try:
            file_path = unquote(request.query_params.get("path", ""))
            if not file_path:
                return Response(
                    status_code=400,
                    description=json.dumps({"error": "Missing 'path' parameter"}),
                    headers={"Content-Type": "application/json"},
                )

            data = await storage_service.get_file(file_path)
            if data is None:
                return Response(
                    status_code=404,
                    description=json.dumps({"error": "File not found"}),
                    headers={"Content-Type": "application/json"},
                )

            content_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
            filename = file_path.rsplit("/", 1)[-1]

            return Response(
                status_code=200,
                description=data,
                headers={
                    "Content-Type": content_type,
                    "Content-Disposition": f'attachment; filename="{filename}"',
                    "Content-Length": str(len(data)),
                },
            )
        except Exception as e:
            return Response(
                status_code=500,
                description=json.dumps({"error": str(e)}),
                headers={"Content-Type": "application/json"},
            )

    @app.delete("/api/v1/media/files")
    async def delete_file(request):
        """Delete a media file by its relative path (passed as ?path=...)."""
        try:
            file_path = unquote(request.query_params.get("path", ""))
            if not file_path:
                return Response(
                    status_code=400,
                    description=json.dumps({"error": "Missing 'path' parameter"}),
                    headers={"Content-Type": "application/json"},
                )
            success = await storage_service.delete_file(file_path)
            return json.dumps({"success": success})
        except Exception as e:
            return Response(
                status_code=500,
                description=json.dumps({"error": str(e)}),
                headers={"Content-Type": "application/json"},
            )

    @app.get("/api/v1/media/sync/status")
    async def get_sync_status(request):
        """Get cloud sync status."""
        try:
            status = await storage_service.get_sync_status()
            return json.dumps(status.model_dump(mode="json"))
        except Exception as e:
            return Response(
                status_code=500,
                description=json.dumps({"error": str(e)}),
                headers={"Content-Type": "application/json"},
            )

    @app.post("/api/v1/media/sync/start")
    async def start_sync(request):
        """Start cloud sync."""
        try:
            success = await storage_service.start_sync()
            return json.dumps({"success": success})
        except Exception as e:
            return Response(
                status_code=500,
                description=json.dumps({"error": str(e)}),
                headers={"Content-Type": "application/json"},
            )
