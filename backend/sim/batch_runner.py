import os, json

from backend.sim.scenario_loader import load_scenario, list_scenarios
from backend.sim.digital_twin import run_simulation

SCENARIO_DIR = "/opt/ptp-data/scenarios"

def summarize_results(results):
    """
    Compute summary metrics for a simulation run.
    """
    timing = [r["timing_output"] for r in results]
    if not timing:
        return {
            "max_error": 0,
            "min_error": 0,
            "rms_error": 0
        }

    import numpy as np
    arr = np.array(timing)

    return {
        "max_error": float(arr.max()),
        "min_error": float(arr.min()),
        "rms_error": float(np.sqrt(np.mean(arr**2)))
    }

def run_batch():
    batch_results = []

    for scenario_file in list_scenarios():
        scenario = load_scenario(scenario_file)
        base_day = scenario["base_day"]

        base_path = f"/opt/ptp-data/live/{base_day}/gnss_samples.json"
        if not os.path.exists(base_path):
            continue

        with open(base_path) as f:
            samples = json.load(f)

        sim_results = run_simulation(samples, scenario)
        summary = summarize_results(sim_results)

        batch_results.append({
            "scenario": scenario_file,
            "summary": summary
        })

    return batch_results
