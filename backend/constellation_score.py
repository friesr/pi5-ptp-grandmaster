from flask import Blueprint, jsonify
import os, csv
from backend.analysis.constellation_score import score_constellation

constellation_score_api = Blueprint("constellation_score_api", __name__)

@constellation_score_api.route("/load/<day>")
def load_constellation_scores(day):
    base = f"/opt/ptp-data/live/{day}"
    file = os.path.join(base, "gnss.csv")

    if not os.path.exists(file):
        return jsonify([])

    rows = []
    with open(file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({
                "prn": int(row["prn"]),
                "snr": float(row["snr"]),
                "elevation": float(row["elevation"]),
                "used": row["used"] == "1",
                "constellation": row["constellation"]
            })

    scores = score_constellation(rows)
    return jsonify(scores)
