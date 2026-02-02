from flask import Blueprint, jsonify
import os
import csv

from backend.analysis.gnss_outages import detect_outages

gnss_outages_api = Blueprint("gnss_outages_api", __name__)


@gnss_outages_api.route("/load/<day>")
def load_outages(day):
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
                "used_count": int(row["used_count"]),
                "visible_count": int(row["visible_count"])
            })

    outages = detect_outages(rows)
    return jsonify(outages)
