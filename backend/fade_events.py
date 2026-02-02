from flask import Blueprint, jsonify
import os, csv
from backend.analysis.fade_events import detect_fade_events

fade_events_api = Blueprint("fade_events_api", __name__)

@fade_events_api.route("/load/<day>")
def load_fade_events(day):
    base = f"/opt/ptp-data/live/{day}"
    file = os.path.join(base, "gnss.csv")

    if not os.path.exists(file):
        return jsonify([])

    rows = []
    with open(file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({
                "timestamp": float(row["timestamp"]),
                "prn": int(row["prn"]),
                "snr": float(row["snr"]),
                "used": row["used"] == "1"
            })

    events = detect_fade_events(rows)
    return jsonify(events)
