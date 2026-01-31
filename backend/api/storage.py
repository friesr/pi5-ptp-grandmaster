from flask import Blueprint, jsonify
from backend.storage.manager import get_directory_size_gb
from backend.config.manager import load_config

storage_api = Blueprint("storage_api", __name__)

@storage_api.route("/status")
def storage_status():
    cfg = load_config()
    local = get_directory_size_gb("/opt/ptp-data/live")
    nas = get_directory_size_gb("/opt/ptp-data/archive")
    return jsonify({
        "local": {
            "used_gb": local,
            "max_gb": cfg["local_max_gb"],
            "percent": (local / cfg["local_max_gb"]) * 100
        },
        "nas": {
            "used_gb": nas,
            "max_gb": cfg["nas_max_gb"],
            "percent": (nas / cfg["nas_max_gb"]) * 100
        }
    })
