from flask import Blueprint, jsonify
import os, json

from backend.analysis.report_builder import build_report

report_api = Blueprint("report_api", __name__)

@report_api.route("/daily/<day>")
def daily_report(day):
    base = f"/opt/ptp-data/live/{day}"

    def load(name):
        file = os.path.join(base, name)
        return json.load(open(file)) if os.path.exists(file) else {}

    metrics = load("daily_metrics.json")
    sla = load("sla_report.json")
    timeline = load("unified_timeline.json")
    predictions = load("predictive_maintenance.json")
    env_change = load("environment_change.json")
    confidence = load("timing_confidence.json").get("score", 0)

    report = build_report(day, metrics, sla, timeline, predictions, env_change, confidence)
    return jsonify(report)
