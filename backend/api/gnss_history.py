from flask import Blueprint, jsonify
import os
import csv

gnss_history_api = Blueprint("gnss_history_api", __name__)

@gnss_history_api.route("/days")
def list_days():
    path = "/opt/ptp-data/live"
    if not os.path.exists(path):
        return jsonify([])
    return jsonify(sorted(os.listdir(path)))

@gnss_history_api.route("/load/<day>")
def load_day(day):
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
                "snr": float(row["snr"])
            })

    return jsonify(rows)
