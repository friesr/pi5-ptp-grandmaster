from flask import Blueprint, jsonify
import os, json

from backend.sim.scenario_loader import load_scenario
from backend.sim.digital_twin import run_simulation
from backend.sim.event_annotator import detect_events

digital_twin_event_timeline_api = Blueprint("digital_twin_event_timeline_api", __name__)

@digital_twin_event_timeline_api.route("/run/<scenario_name>")
def run(scenario_name):
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
    events = detect_events(results)

    return jsonify({
        "scenario": scenario_name,
        "events": events
    })
