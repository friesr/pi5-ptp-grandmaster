from flask import Blueprint, jsonify
import os, json

from backend.analysis.sla_engine import evaluate_sla

sla_api = Blueprint("sla_api", __name__)

@sla_api.route("/load/<day>")
def load_sla(day):
    base = f"/opt/ptp-data/live/{day}"

    sla = json.load(open("backend/config/sla.json"))

    metrics_file = os.path.join(base, "daily_metrics.json")
    if not os.path.exists(metrics_file):
        return jsonify({"error": "missing metrics"})

    metrics = json.load(open(metrics_file))

    result = evaluate_sla(sla, metrics)
    return jsonify(result)
