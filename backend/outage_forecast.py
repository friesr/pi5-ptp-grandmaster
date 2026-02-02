from flask import Blueprint, jsonify
import os, json

from backend.analysis.outage_features import extract_outage_features
from backend.analysis.outage_probability import compute_outage_probability

outage_forecast_api = Blueprint("outage_forecast_api", __name__)

@outage_forecast_api.route("/predict/<day>")
def predict(day):
    base = f"/opt/ptp-data/live/{day}"

    def load(name):
        file = os.path.join(base, name)
        return json.load(open(file)) if os.path.exists(file) else {}

    day_summary = load("daily_summary.json")
    constellation_forecast = load("constellation_forecast.json")
    aging = load("satellite_aging.json")
    interference = load("interference_summary.json")
    env_dev = load("environment_change.json").get("deviation", 0)
    timing_pred = load("stability_prediction.json")

    if not constellation_forecast or not aging:
        return jsonify({"error": "missing forecast or aging data"})

    features = extract_outage_features(day_summary, constellation_forecast, aging, interference, env_dev, timing_pred)
    probability = compute_outage_probability(features)

    return jsonify({
        "features": features,
        "outage_probability": probability
    })
