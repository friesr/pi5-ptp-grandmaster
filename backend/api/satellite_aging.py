from flask import Blueprint, jsonify
import os, json

from backend.analysis.satellite_aging_features import extract_aging_features
from backend.analysis.satellite_aging import compute_aging

satellite_aging_api = Blueprint("satellite_aging_api", __name__)

@satellite_aging_api.route("/analyze")
def analyze():
    base = "/opt/ptp-data/live"

    history = []
    for day in sorted(os.listdir(base)):
        file = os.path.join(base, day, "daily_summary.json")
        if os.path.exists(file):
            history.append(json.load(open(file)))

    if not history:
        return jsonify({"error": "no history"})

    prn_data = extract_aging_features(history)
    aging = compute_aging(prn_data)

    return jsonify(aging)
