from flask import Blueprint, jsonify
import os, json

from backend.analysis.clock_stability_features import extract_clock_features
from backend.analysis.clock_stability import compute_clock_stability

clock_api = Blueprint("clock_api", __name__)

@clock_api.route("/analyze/<day>")
def analyze(day):
    base = f"/opt/ptp-data/live/{day}"
    file = os.path.join(base, "gnss_samples.json")

    if not os.path.exists(file):
        return jsonify({"error": "no GNSS samples"})

    samples = json.load(open(file))
    prn_data = extract_clock_features(samples)
    stats = compute_clock_stability(prn_data)

    return jsonify(stats)
