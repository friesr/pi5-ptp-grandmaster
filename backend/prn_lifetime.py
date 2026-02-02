from flask import Blueprint, jsonify
import os, csv
from backend.analysis.prn_lifetime import compute_prn_lifetimes

prn_lifetime_api = Blueprint("prn_lifetime_api", __name__)

@prn_lifetime_api.route("/load/<day>")
def load_prn_lifetime(day):
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
                "visible": row["visible"] == "1",
                "used": row["used"] == "1"
            })

    lifetimes = compute_prn_lifetimes(rows)
    return jsonify(lifetimes)
