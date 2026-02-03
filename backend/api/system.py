from flask import Blueprint, jsonify

system_bp = Blueprint("system", __name__)

@system_bp.route("/health", methods=["GET"])
def system_health():
    return jsonify({
        "status": "ok",
        "uptime": "unknown",
        "message": "System backend responding"
    })
