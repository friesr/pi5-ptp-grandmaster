from flask import Blueprint, jsonify
import os, json

from backend.analysis.spoofing_features import extract_spoofing_features
from backend.analysis.spoofing_classifier import classify_spoofing

spoofing_api = Blueprint("spoofing_api", __name__)

@spoofing_api.route("/detect/<day>")
def detect_spoofing(day):
    base = f"/opt/ptp-data/live/{day}"

    def load(name):
        file = os.path.join(base, name)
        return json.load(open(file)) if os.path.exists(file) else {}

    a = load("receiverA_summary.json")
    b = load("receiverB_summary.json")
    constellation_perf = load("constellation_performance.json")
    env_dev = load("environment_change.json").get("deviation", 0)
    timing = load("stability_prediction.json")
    interference = load("interference_summary.json")

    if not a or not b:
        return jsonify({"error": "receiver data missing"})

    features = extract_spoofing_features(a, b, constellation_perf, env_dev, timing, interference)
    classification = classify_spoofing(features)

    return jsonify({
        "features": features,
        "classification": classification
    })
