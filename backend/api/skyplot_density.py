from flask import Blueprint, jsonify
import os, csv
from backend.analysis.skyplot_density import build_skyplot_density

skyplot_density_api = Blueprint("skyplot_density_api", __name__)

@skyplot_density_api.route("/load/<day>")
def load_density(day):
    base = f"/opt/ptp-data/live/{day}"
    file = os.path.join(base, "gnss.csv")

    if not os.path.exists(file):
        return jsonify([])

    rows = []
    with open(file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({
                "azimuth": float(row["azimuth"]),
                "elevation": float(row["elevation"])
            })

    density = build_skyplot_density(rows)
    return jsonify(density)
