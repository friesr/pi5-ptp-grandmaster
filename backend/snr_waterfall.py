from flask import Blueprint, jsonify
import os, csv
from backend.analysis.snr_waterfall import build_snr_waterfall

snr_waterfall_api = Blueprint("snr_waterfall_api", __name__)

@snr_waterfall_api.route("/load/<day>")
def load_waterfall(day):
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
                "prn": int(row["prn"]),
                "snr": float(row["snr"])
            })

    prns, times, matrix = build_snr_waterfall(rows)
    return jsonify({
        "prns": prns,
        "times": times,
        "matrix": matrix
    })
