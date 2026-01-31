from flask import Blueprint, jsonify
from backend.storage.manager import get_directory_size_gb
from backend.storage.archive import archive_old_files
from backend.config.manager import load_config

storage_api = Blueprint("storage_api", __name__)

@storage_api.route("/status")
def storage_status():
    cfg = load_config()
    local = get_directory_size_gb("/opt/ptp-data/live")
    nas = get_directory_size_gb("/opt/ptp-data/archive")

    return jsonify({
        "local": {
            "used_gb": round(local, 3),
            "max_gb": cfg["local_max_gb"],
            "percent": round((local / cfg["local_max_gb"]) * 100, 2)
        },
        "nas": {
            "used_gb": round(nas, 3),
            "max_gb": cfg["nas_max_gb"],
            "percent": round((nas / cfg["nas_max_gb"]) * 100, 2)
        }
    })

@storage_api.route("/archive", methods=["POST"])
def run_archive():
    result = archive_old_files()
    return jsonify(result)
