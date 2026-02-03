from flask import Blueprint, jsonify

system_global_bp = Blueprint("system_global", __name__)

@system_global_bp.route("/health", methods=["GET"])
def global_system_health():
    return jsonify({
        "status": "ok",
        "message": "Global system health endpoint responding"
    })
