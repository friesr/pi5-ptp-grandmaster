from flask import Blueprint, jsonify
import os, json

from backend.analysis.constellation_performance import compute_constellation_performance

constellation_perf_api = Blueprint("constellation_perf_api", __name__)

@constellation_perf_api.route("/load")
def load_constellation_perf():
    base = "/opt/ptp-data/live"

    history = []
    for day in sorted(os.listdir(base)):
        file = os.path.join(base, day, "daily_summary.json")
        if os.path.exists(file):
            history.append(json.load(open(file)))

    if not history:
        return jsonify({"error": "no history"})

    perf = compute_constellation_performance(history)
    return jsonify(perf)
