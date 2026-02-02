from flask import Blueprint, jsonify
from backend.sim.sensitivity_runner import run_sensitivity

sensitivity_api = Blueprint("sensitivity_api", __name__)

@sensitivity_api.route("/run/<sweep_file>")
def run(sweep_file):
    path = f"/opt/ptp-data/scenarios/{sweep_file}"
    results = run_sensitivity(path)
    return jsonify(results)
