from flask import Blueprint, jsonify
import os, json

from backend.analysis.resilience_context import build_resilience_context
from backend.analysis.resilience_recommendations import generate_recommendations

resilience_api = Blueprint("resilience_api", __name__)

@resilience_api.route("/advise/<day>")
def advise(day):
    base = f"/opt/ptp-data/live/{day}"

    def load(name):
        file = os.path.join(base, name)
        return json.load(open(file)) if os.path.exists(file) else {}

    root_cause = load("sla_root_cause.json")
    outage_forecast = load("outage_forecast.json")
    timing_pred = load("stability_prediction.json")
    interference = load("interference_summary.json")
    env_dev = load("environment_change.json").get("deviation", 0)
    siting = load("antenna_siting.json")
    receiver_health = load("receiver_health.json")

    if not root_cause:
        return jsonify({"error": "missing root cause data"})

    ctx = build_resilience_context(
        root_cause,
        outage_forecast.get("outage_probability", 0),
        timing_pred,
        interference,
        env_dev,
        siting,
        receiver_health
    )

    recs = generate_recommendations(ctx)

    return jsonify({
        "context": ctx,
        "recommendations": recs
    })
