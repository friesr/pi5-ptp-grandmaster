from flask import Blueprint, jsonify
import os, json

from backend.analysis.stability_features import build_stability_features
from backend.analysis.stability_predictor import train_stability_model, predict_stability

stability_api = Blueprint("stability_api", __name__)

@stability_api.route("/predict")
def predict_stability_api():
    base = "/opt/ptp-data/live"

    history = []
    for day in sorted(os.listdir(base)):
        file = os.path.join(base, day, "daily_summary.json")
        if os.path.exists(file):
            history.append(json.load(open(file)))

    if len(history) < 3:
        return jsonify({"error": "not enough history"})

    X, y = build_stability_features(history)
    model = train_stability_model(X, y)

    today = history[-1]
    today_features = [
        today["timing_error_avg"],
        today["timing_confidence"],
        today["geometry_score"],
        today["avg_snr"],
        today["avg_multipath"],
        today["prn_health_avg"],
        today["interference_count"],
        today["env_deviation"],
        today["receiver_health_score"]
    ]

    prediction = predict_stability(model, today_features)

    return jsonify({
        "predicted_timing_error_ns": prediction,
        "risk_level": (
            "low" if prediction < 50 else
            "moderate" if prediction < 150 else
            "high"
        )
    })
