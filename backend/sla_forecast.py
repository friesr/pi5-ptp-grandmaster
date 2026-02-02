from flask import Blueprint, jsonify
import os, json

from backend.analysis.sla_features import extract_sla_features
from backend.analysis.sla_probability import compute_sla_probability

sla_forecast_api = Blueprint("sla_forecast_api", __name__)

@sla_forecast_api.route("/predict/<day>")
def predict(day):
    base = f"/opt/ptp-data/live/{day}"

    def load(name):
        file = os.path.join(base, name)
        return json.load(open(file)) if os.path.exists(file) else {}

    day_summary = load("daily_summary.json")
    outage_prob = load("outage_forecast.json").get("outage_probability", 0)
    timing_pred = load("stability_prediction.json")
    interference = load("interference_summary.json")
    env_dev = load("environment_change.json").get("deviation", 0)
    constellation_forecast = load("constellation_forecast.json")
    aging = load("satellite_aging.json")

    if not constellation_forecast or not aging:
        return jsonify({"error": "missing forecast or aging data"})

    features = extract_sla_features(day_summary, outage_prob, timing_pred, interference, env_dev, constellation_forecast, aging)
    probability = compute_sla_probability(features)

    return jsonify({
        "features": features,
        "sla_violation_probability": probability
    })
