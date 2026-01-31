from flask import Blueprint, jsonify
import os

history_api = Blueprint("history_api", __name__)

@history_api.route("/days")
def list_days():
    path = "/opt/ptp-data/live"
    if not os.path.exists(path):
        return jsonify([])

    days = sorted(os.listdir(path))
    return jsonify(days)
