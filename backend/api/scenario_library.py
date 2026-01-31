from flask import Blueprint, jsonify
import os

LIB_DIR = "/opt/ptp-data/scenarios/library"

scenario_library_api = Blueprint("scenario_library_api", __name__)

@scenario_library_api.route("/list")
def list_library():
    out = {}
    for root, dirs, files in os.walk(LIB_DIR):
        category = os.path.basename(root)
        out[category] = [f for f in files if f.endswith(".json")]
    return jsonify(out)
