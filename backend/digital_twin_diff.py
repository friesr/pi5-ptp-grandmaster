from flask import Blueprint, request, jsonify
import os, json

from backend.sim.scenario_loader import load_scenario
from backend.sim.digital_twin import run_simulation
from backend.sim.scenario_diff import diff_scenarios

digital_twin_diff_api = Blueprint("digital_twin_diff_api", __name__)

@digital_twin_diff_api.route("/run", methods=["POST"])
def run():
    data = request.json
    a_name = data.get("scenario_a")
    b_name = data.get("scenario_b")

    # Load scenarios
    sa = load_scenario(a_name)
    sb = load_scenario(b_name)

    if not sa or not sb:
        return jsonify({"error": "scenario not found"})

    # Load samples
    def load_samples(day):
        path = f"/opt/ptp-data/live/{day}/gnss_samples.json"
        if not os.path.exists(path):
            return None
        with open(path) as f:
            return json.load(f)

    samples_a = load_samples(sa["base_day"])
    samples_b = load_samples(sb["base_day"])

    if samples_a is None or samples_b is None:
        return jsonify({"error": "base day samples missing"})

    # Run simulations
    results_a = run_simulation(samples_a, sa)
    results_b = run_simulation(samples_b, sb)

    # Compute diff
    diff = diff_scenarios(results_a, results_b)

    return jsonify(diff)
