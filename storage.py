"""Storage helpers for extension-safe file access."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import bpy


def get_extension_user_dir(create: bool = True) -> str:
    """Return the writable user directory for this extension package."""
    try:
        return bpy.utils.extension_path_user(__package__, path="", create=create)
    except AttributeError:
        # Fallback for older Blender versions that do not expose extension_path_user.
        fallback = bpy.utils.user_resource(
            'SCRIPTS',
            path=f"addons/{__package__}",
            create=create,
        )
        return fallback


def append_extension_log(message: str) -> None:
    """Append a timestamped line to the extension log in user storage."""
    user_dir = Path(get_extension_user_dir(create=True))
    user_dir.mkdir(parents=True, exist_ok=True)
    log_file = user_dir / "nebula_uv_manager.log"
    timestamp = datetime.utcnow().isoformat(timespec="seconds")
    log_file.write_text(
        (
            log_file.read_text(encoding="utf-8") if log_file.exists() else ""
        )
        + f"[{timestamp}Z] {message}\n",
        encoding="utf-8",
    )
