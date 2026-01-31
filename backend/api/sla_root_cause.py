from flask import Blueprint, jsonify
import os, json

from backend.analysis.sla_root_cause_features import fuse_root_cause_features
from backend.analysis.sla_root_cause_explainer import explain_root_cause

sla_root_api = Blueprint("sla_root_api", __name__)

@sla_root_api.route("/explain/<day>")
def explain(day):
    base = f"/opt/ptp-data/live/{day}"

    def load(name):
        file = os.path.join(base, name)
        return json.load(open(file)) if os.path.exists(file) else {}

    sla_forecast = load("sla_forecast.json")
    outage_forecast = load("outage_forecast.json")

    if not sla_forecast or not outage_forecast:
        return jsonify({"error": "missing forecast data"})

    fused = fuse_root_cause_features(sla_forecast, outage_forecast)
    explanation = explain_root_cause(fused)

    return jsonify({
        "sla_violation_probability": fused["sla_violation_probability"],
        "root_causes": explanation
    })
