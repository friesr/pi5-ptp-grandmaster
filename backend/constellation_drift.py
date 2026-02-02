from flask import Blueprint, jsonify
import os, csv

from backend.analysis.constellation_drift import compute_daily_stats, compute_drift

constellation_drift_api = Blueprint("constellation_drift_api", __name__)

@constellation_drift_api.route("/load")
def load_drift():
    base = "/opt/ptp-data/live"

    if not os.path.exists(base):
        return jsonify({})

    days = sorted(os.listdir(base))
    history = []

    for day in days:
        file = os.path.join(base, day, "gnss.csv")
        if not os.path.exists(file):
            continue

        rows = []
        with open(file) as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append({
                    "constellation": row["constellation"],
                    "snr": float(row["snr"])
                })

        history.append(compute_daily_stats(rows))

    drift = compute_drift(history)

    return jsonify({
        "days": days,
        "history": history,
        "drift": drift
    })
