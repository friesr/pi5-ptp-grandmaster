import json
import numpy as np
import os
import itertools

from backend.sim.scenario_loader import load_scenario
from backend.sim.digital_twin import run_simulation
from backend.sim.batch_runner import summarize_results

def linspace(min_val, max_val, steps):
    return np.linspace(min_val, max_val, steps).tolist()

def generate_candidates(search_space):
    param_lists = {}

    for key, spec in search_space.items():
        if isinstance(spec, dict):
            param_lists[key] = linspace(spec["min"], spec["max"], spec["steps"])
        else:
            param_lists[key] = spec

    keys = list(param_lists.keys())
    values = [param_lists[k] for k in keys]

    for combo in itertools.product(*values):
        yield dict(zip(keys, combo))

def optimize(opt_file):
    with open(opt_file) as f:
        opt_def = json.load(f)

    base_scenario = load_scenario(opt_def["scenario_name"])
    search_space = opt_def["search_space"]
    objective = opt_def["objective"]

    base_day = base_scenario["base_day"]
    path = f"/opt/ptp-data/live/{base_day}/gnss_samples.json"

    if not os.path.exists(path):
        return []

    with open(path) as f:
        samples = json.load(f)

    results = []

    for params in generate_candidates(search_space):
        scenario = json.loads(json.dumps(base_scenario))  # deep copy

        # Apply parameters
        for k, v in params.items():
            if k in ["kp", "ki"]:
                scenario["servo_adjustments"][k] = v
            elif k == "interference_mitigation":
                scenario["perturbations"]["interference"]["mitigation"] = v
            elif k == "spoofing_threshold":
                scenario["perturbations"]["spoofing"]["threshold"] = v

        sim_results = run_simulation(samples, scenario)
        summary = summarize_results(sim_results)

        score = summary["rms_error"] if objective == "minimize_rms_error" else summary["max_error"]

        results.append({
            "parameters": params,
            "summary": summary,
            "score": score
        })

    # Sort by score (lower is better)
    results.sort(key=lambda r: r["score"])

    return results[:10]  # top 10
