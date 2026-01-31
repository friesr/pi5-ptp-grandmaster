from flask import Blueprint, jsonify
import os
import json

from backend.analysis.eclipse_stats import build_eclipse_stats

eclipse_api = Blueprint("eclipse_api", __name__)

@eclipse_api.route("/analyze/<day>")
def analyze(day):
    base = f"/opt/ptp-data/live/{day}"
    file = os.path.join(base, "gnss_samples.json")

    if not os.path.exists(file):
        return jsonify({"error": "no GNSS samples"})

    with open(file) as f:
        samples = json.load(f)

    stats = build_eclipse_stats(samples)
    return jsonify(stats)
