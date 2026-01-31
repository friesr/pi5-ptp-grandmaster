from flask import Blueprint, jsonify
import os, csv
from backend.analysis.geometry_score import compute_geometry_score

geometry_timeline_api = Blueprint("geometry_timeline_api", __name__)

@geometry_timeline_api.route("/load/<day>")
def load_geometry(day):
    base = f"/opt/ptp-data/live/{day}"
    file = os.path.join(base, "gnss.csv")

    if not os.path.exists(file):
        return jsonify([])

    out = []

    with open(file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            gdop = float(row["gdop"])
            pdop = float(row["pdop"])
            hdop = float(row["hdop"])
            vdop = float(row["vdop"])
            tdop = float(row["tdop"])

            scores = compute_geometry_score(gdop, pdop, hdop, vdop, tdop)

            out.append({
                "timestamp": float(row["timestamp"]),
                **scores
            })

    return jsonify(out)
