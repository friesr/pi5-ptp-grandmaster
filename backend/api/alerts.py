from flask import Blueprint, jsonify
from backend.api.status import get_status_snapshot  # you already effectively have this logic
from backend.alerts.engine import evaluate_alerts

alerts_api = Blueprint("alerts_api", __name__)

@alerts_api.route("/current")
def current_alerts():
    status = get_status_snapshot()
    alerts = evaluate_alerts(status)
    return jsonify(alerts)
