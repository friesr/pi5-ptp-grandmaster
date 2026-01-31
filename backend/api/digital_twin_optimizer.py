from flask import Blueprint, jsonify
from backend.sim.optimizer import optimize

digital_twin_optimize_api = Blueprint("digital_twin_optimize_api", __name__)

@digital_twin_optimize_api.route("/run/<opt_file>")
def run(opt_file):
    path = f"/opt/ptp-data/scenarios/{opt_file}"
    results = optimize(path)
    return jsonify(results)
