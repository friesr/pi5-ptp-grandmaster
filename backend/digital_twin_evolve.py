from flask import Blueprint, jsonify
from backend.sim.ga_runner import run_ga

digital_twin_evolve_api = Blueprint("digital_twin_evolve_api", __name__)

@digital_twin_evolve_api.route("/run/<config_file>")
def run(config_file):
    path = f"/opt/ptp-data/scenarios/{config_file}"
    results = run_ga(path)
    return jsonify(results)
