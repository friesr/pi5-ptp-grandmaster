from flask import Blueprint, jsonify
import os, json

from backend.sim.scenario_loader import load_scenario
from backend.sim.digital_twin import run_simulation
from backend.sim.batch_runner import summarize_results
from backend.sim.report_builder import build_report

digital_twin_report_api = Blueprint("digital_twin_report_api", __name__)

@digital_twin_report_api.route("/generate/<scenario_name>")
def generate(scenario_name):
    scenario = load_scenario(scenario_name)
    if not scenario:
        return jsonify({"error": "scenario not found"})

    base_day = scenario["base_day"]
    base_path = f"/opt/ptp-data/live/{base_day}/gnss_samples.json"

    if not os.path.exists(base_path):
        return jsonify({"error": "base day samples not found"})

    with open(base_path) as f:
        samples = json.load(f)

    results = run_simulation(samples, scenario)
    summary = summarize_results(results)
    report = build_report(scenario, results, summary)

    return jsonify(report)
