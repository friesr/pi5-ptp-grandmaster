from flask import Blueprint, jsonify
import os, json

from backend.analysis.predictive_maintenance import build_predictive_maintenance

predictive_api = Blueprint("predictive_api", __name__)

@predictive_api.route("/load")
def load_predictive():
    base = "/opt/ptp-data/live"

    history = []

    for day in sorted(os.listdir(base)):
        file = os.path.join(base, day, "daily_summary.json")
        if os.path.exists(file):
            history.append(json.load(open(file)))

    if not history:
        return jsonify({"error": "no history"})

    result = build_predictive_maintenance(history)
    return jsonify(result)
