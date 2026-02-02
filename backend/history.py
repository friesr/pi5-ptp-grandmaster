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

import csv

@history_api.route("/load/<day>")
def load_day(day):
    base = f"/opt/ptp-data/live/{day}"

    def load_csv(name):
        file = os.path.join(base, name)
        if not os.path.exists(file):
            return []
        rows = []
        with open(file) as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
        return rows

    return jsonify({
        "ptp": load_csv("ptp.csv"),
        "ntp": load_csv("ntp.csv"),
        "gnss": load_csv("gnss.csv"),
        "system": load_csv("system.csv")
    })
