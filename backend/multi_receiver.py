from flask import Blueprint, jsonify
import os, json

from backend.analysis.multi_receiver_features import extract_correlation_features
from backend.analysis.multi_receiver_classifier import classify_correlation

multi_api = Blueprint("multi_api", __name__)

@multi_api.route("/compare/<day>")
def compare_receivers(day):
    base = f"/opt/ptp-data/live/{day}"

    def load(name):
        file = os.path.join(base, name)
        return json.load(open(file)) if os.path.exists(file) else None

    a = load("receiverA_summary.json")
    b = load("receiverB_summary.json")

    if not a or not b:
        return jsonify({"error": "missing receiver data"})

    features = extract_correlation_features(a, b)
    classification = classify_correlation(features)

    return jsonify({
        "features": features,
        "classification": classification
    })
