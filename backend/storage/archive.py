from backend.storage.manager import (
    enforce_local_limit,
    move_oldest_to_archive
)
from backend.config.manager import load_config

def archive_old_files():
    cfg = load_config()

    local_path = "/opt/ptp-data/live"
    archive_path = "/opt/ptp-data/archive"

    moved = move_oldest_to_archive(
        local_path,
        archive_path,
        cfg["nas_max_gb"]
    )

    removed = enforce_local_limit(
        local_path,
        cfg["local_max_gb"]
    )

    return {
        "moved_to_archive": moved,
        "deleted_local": removed
    }
