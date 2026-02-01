from flask import Blueprint, jsonify

system_api = Blueprint("system_api", __name__)

@system_api.route("/api/system/health", methods=["GET"])
def system_health():
    return jsonify({
        "status": "ok",
        "backend": "running",
        "version": "1.0"
    })
