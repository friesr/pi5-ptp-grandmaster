from flask import Blueprint, request, jsonify
from backend.ptp.profiles import PTP_PROFILES
from backend.config.manager import load_config, save_config
import subprocess

ptp_profile_api = Blueprint("ptp_profile_api", __name__)

def write_ptp4l_config(profile):
    path = "/etc/ptp4l.conf"
    with open(path, "w") as f:
        f.write("[global]\n")
        for k, v in profile["ptp4l"].items():
            f.write(f"{k} {v}\n")

def write_phc2sys_config(profile):
    path = "/etc/phc2sys.conf"
    with open(path, "w") as f:
        f.write("[global]\n")
        f.write(f"sync_interval {profile['phc2sys']['sync_interval']}\n")

def restart_services():
    subprocess.call(["systemctl", "restart", "ptp4l"])
    subprocess.call(["systemctl", "restart", "phc2sys"])

@ptp_profile_api.route("/apply", methods=["POST"])
def apply_profile():
    data = request.json
    name = data.get("profile")

    if name not in PTP_PROFILES:
        return jsonify({"error": "unknown_profile"}), 400

    profile = PTP_PROFILES[name]

    write_ptp4l_config(profile)
    write_phc2sys_config(profile)
    restart_services()

    cfg = load_config()
    cfg["ptp_profile"] = name
    save_config(cfg)

    return jsonify({"status": "ok", "applied": name})
