from flask import Blueprint, jsonify
import os, json

from backend.analysis.unified_timeline import build_unified_timeline

unified_api = Blueprint("unified_api", __name__)

@unified_api.route("/load/<day>")
def load_unified(day):
    base = f"/opt/ptp-data/live/{day}"

    def load(name):
        file = os.path.join(base, name)
        return json.load(open(file)) if os.path.exists(file) else []

    gnss = load("gnss_events.json")
    ptp = load("ptp_events.json")
    inter = load("interference.json")
    sla = load("sla_violations.json")
    recv = load("receiver_events.json")
    env = load("environment_changes.json")

    timeline = build_unified_timeline(gnss, ptp, inter, sla, recv, env)
    return jsonify(timeline)
