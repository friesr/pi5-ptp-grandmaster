from flask import Blueprint, jsonify
import os, csv
from backend.analysis.constellation_timeline import build_constellation_timeline

constellation_timeline_api = Blueprint("constellation_timeline_api", __name__)

@constellation_timeline_api.route("/load/<day>")
def load_timeline(day):
    base = f"/opt/ptp-data/live/{day}"
    file = os.path.join(base, "gnss.csv")

    if not os.path.exists(file):
        return jsonify({})

    rows = []
    with open(file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({
                "timestamp": float(row["timestamp"]),
                "constellation": row["constellation"],
                "used": row["used"] == "1"
            })

    timeline = build_constellation_timeline(rows)
    return jsonify(timeline)
