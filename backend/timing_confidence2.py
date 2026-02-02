from flask import Blueprint, jsonify
import os, json

from backend.analysis.timing_confidence2_features import fuse_confidence_features
from backend.analysis.timing_confidence2 import compute_timing_confidence2

timing_conf2_api = Blueprint("timing_conf2_api", __name__)

@timing_conf2_api.route("/compute/<day>")
def compute(day):
    base = f"/opt/ptp-data/live/{day}"

    def load(name):
        file = os.path.join(base, name)
        return json.load(open(file)) if os.path.exists(file) else {}

    timing_pred = load("stability_prediction.json")
    outage = load("outage_forecast.json")
    sla = load("sla_forecast.json")
    constellation_forecast = load("constellation_forecast.json")
    aging = load("satellite_aging.json")
    clock_stats = load("clock_stability.json")
    interference = load("interference_summary.json")
    env_dev = load("environment_change.json").get("deviation", 0)
    multipath = load("multipath_summary.json")
    receiver_health = load("receiver_health.json")
    spoofing = load("spoofing.json")

    features = fuse_confidence_features(
        timing_pred,
        outage.get("outage_probability", 0),
        sla.get("sla_violation_probability", 0),
        constellation_forecast,
        aging,
        clock_stats,
        interference,
        env_dev,
        multipath,
        receiver_health,
        spoofing
    )

    score = compute_timing_confidence2(features)

    return jsonify({
        "confidence_score": score,
        "features": features
    })
