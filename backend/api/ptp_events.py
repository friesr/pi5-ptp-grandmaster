from flask import Blueprint, jsonify
import os

from backend.analysis.ptp_events import parse_ptp_events

ptp_events_api = Blueprint("ptp_events_api", __name__)

@ptp_events_api.route("/load/<day>")
def load_ptp_events(day):
    base = f"/opt/ptp-data/live/{day}"
    file = os.path.join(base, "ptp4l.log")

    if not os.path.exists(file):
        return jsonify([])

    with open(file) as f:
        lines = f.readlines()

    events = parse_ptp_events(lines)
    return jsonify(events)
