from flask import Blueprint, jsonify
from backend.sim.monte_carlo_runner import run_monte_carlo

digital_twin_mc_api = Blueprint("digital_twin_mc_api", __name__)

@digital_twin_mc_api.route("/run/<cfg_file>")
def run(cfg_file):
    path = f"/opt/ptp-data/scenarios/{cfg_file}"
    results = run_monte_carlo(path)
    return jsonify(results)
