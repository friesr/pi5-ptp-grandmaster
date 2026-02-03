from flask import Blueprint, jsonify

global_system_bp = Blueprint("global_system", __name__)

@global_system_bp.route("/health", methods=["GET"])
def global_system_health():
    return jsonify({
        "status": "ok",
        "message": "Global system health endpoint responding"
    })
