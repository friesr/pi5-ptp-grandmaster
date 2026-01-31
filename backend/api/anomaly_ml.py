from flask import Blueprint, jsonify
import os, json

from backend.analysis.anomaly_ml_model import train_anomaly_model, predict_anomaly

anomaly_ml_api = Blueprint("anomaly_ml_api", __name__)

@anomaly_ml_api.route("/predict/<day>")
def predict_ml(day):
    base = f"/opt/ptp-data/live/{day}"

    file = os.path.join(base, "anomaly_clusters.json")
    if not os.path.exists(file):
        return jsonify({"error": "no anomaly data"})

    rows = json.load(open(file))["rows"]

    model = train_anomaly_model(rows)
    if model is None:
        return jsonify({"error": "not enough training data"})

    # Predict for the most recent anomaly
    latest = rows[-1]
    result = predict_anomaly(model, latest)

    return jsonify({
        "timestamp": latest["timestamp"],
        "prediction": result
    })
