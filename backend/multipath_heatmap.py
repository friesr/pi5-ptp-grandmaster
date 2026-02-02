from flask import Blueprint, jsonify
import os, csv
from backend.analysis.multipath_heatmap import build_multipath_heatmap
from backend.analysis.multipath import multipath_score

multipath_heatmap_api = Blueprint("multipath_heatmap_api", __name__)

@multipath_heatmap_api.route("/load/<day>")
def load_heatmap(day):
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
                "elevation": float(row["elevation"]),
                "multipath": multipath_score(float(row["elevation"]), float(row["snr"]))
            })

    heatmap = build_multipath_heatmap(rows)
    return jsonify(heatmap)
