"""DORIS Backend - Utility functions for script deployment."""

import logging
import shutil
from pathlib import Path

FIRMWARE_DIR = Path("/tmp/storage/firmware")
SCRIPTS_DIR = FIRMWARE_DIR / "scripts"
ARTEMIS_SVL_DEST = Path("/usr/bin/artemis_svl.py")

SCRIPT_SEARCH_PATHS = [
    Path("/app/scripts"),
    Path(__file__).resolve().parents[3] / "scripts",
]


def deploy_lua_scripts(logger: logging.Logger) -> None:
    """Copy doris.lua into the ArduPilot scripts folder if the firmware bind-mount exists."""
    if not FIRMWARE_DIR.is_dir():
        logger.info("Firmware directory %s not found, skipping Lua script deployment", FIRMWARE_DIR)
        return

    src: Path | None = None
    for candidate in SCRIPT_SEARCH_PATHS:
        path = candidate / "doris.lua"
        if path.is_file():
            src = path
            break

    if src is None:
        logger.warning("doris.lua not found in any search path: %s", SCRIPT_SEARCH_PATHS)
        return

    try:
        SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
        dest = SCRIPTS_DIR / "doris.lua"
        shutil.copy2(src, dest)
        logger.info("Deployed %s -> %s", src, dest)
    except Exception as e:
        logger.warning("Failed to deploy doris.lua: %s", e)


def deploy_artemis_svl(logger: logging.Logger) -> None:
    """Copy artemis_svl.py to /usr/bin if permissions allow."""
    src: Path | None = None
    for candidate in SCRIPT_SEARCH_PATHS:
        path = candidate / "artemis_svl.py"
        if path.is_file():
            src = path
            break

    if src is None:
        logger.warning("artemis_svl.py not found in any search path: %s", SCRIPT_SEARCH_PATHS)
        return

    try:
        shutil.copy2(src, ARTEMIS_SVL_DEST)
        ARTEMIS_SVL_DEST.chmod(0o755)
        logger.info("Deployed %s -> %s", src, ARTEMIS_SVL_DEST)
    except PermissionError:
        logger.warning("Insufficient permissions to copy artemis_svl.py to %s", ARTEMIS_SVL_DEST)
    except Exception as e:
        logger.warning("Failed to deploy artemis_svl.py: %s", e)
