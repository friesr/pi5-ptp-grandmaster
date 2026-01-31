from flask import Blueprint, request, jsonify
import subprocess

service_control_api = Blueprint("service_control_api", __name__)

SERVICES = [
    "ptp4l",
    "phc2sys",
    "logger.service",
    "alerts.service",
    "dashboard.service"
]

def run_cmd(cmd):
    try:
        subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        return True
    except Exception:
        return False

@service_control_api.route("/list")
def list_services():
    return jsonify(SERVICES)

@service_control_api.route("/status/<name>")
def service_status(name):
    ok = run_cmd(["systemctl", "is-active", "--quiet", name])
    return jsonify({"service": name, "active": ok})

@service_control_api.route("/action", methods=["POST"])
def service_action():
    data = request.json
    name = data.get("service")
    action = data.get("action")

    if name not in SERVICES:
        return jsonify({"error": "unknown_service"}), 400

    if action not in ["start", "stop", "restart"]:
        return jsonify({"error": "invalid_action"}), 400

    ok = run_cmd(["systemctl", action, name])
    return jsonify({"service": name, "action": action, "success": ok})
