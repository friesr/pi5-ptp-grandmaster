from flask import Blueprint, jsonify
import os, json

from backend.analysis.constellation_forecast_features import extract_constellation_timeseries
from backend.analysis.constellation_forecast import forecast_constellations

constellation_forecast_api = Blueprint("constellation_forecast_api", __name__)

@constellation_forecast_api.route("/predict")
def predict():
    base = "/opt/ptp-data/live"

    history = []
    for day in sorted(os.listdir(base)):
        file = os.path.join(base, day, "daily_summary.json")
        if os.path.exists(file):
            history.append(json.load(open(file)))

    if not history:
        return jsonify({"error": "no history"})

    ts = extract_constellation_timeseries(history)
    forecast = forecast_constellations(ts)

    return jsonify(forecast)
