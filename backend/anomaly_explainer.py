from flask import Blueprint, jsonify
import os, json

from backend.analysis.anomaly_explainer import explain_anomaly

anomaly_explainer_api = Blueprint("anomaly_explainer_api", __name__)

@anomaly_explainer_api.route("/load/<day>")
def load_explanations(day):
    base = f"/opt/ptp-data/live/{day}"
    file = os.path.join(base, "anomaly_clusters.json")

    if not os.path.exists(file):
        return jsonify([])

    rows = json.load(open(file))["rows"]

    out = []
    for r in rows:
        out.append({
            "timestamp": r["timestamp"],
            "explanations": explain_anomaly(r)
        })

    return jsonify(out)
