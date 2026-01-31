from flask import Blueprint, request, jsonify
import os, json

SCENARIO_DIR = "/opt/ptp-data/scenarios"

scenario_save_api = Blueprint("scenario_save_api", __name__)

@scenario_save_api.route("/save", methods=["POST"])
def save():
    data = request.json
    name = data.get("scenario_name")

    if not name:
        return jsonify({"error": "scenario_name required"})

    path = os.path.join(SCENARIO_DIR, f"{name}.json")

    with open(path, "w") as f:
        json.dump(data, f, indent=2)

    return jsonify({"status": "saved", "file": f"{name}.json"})
