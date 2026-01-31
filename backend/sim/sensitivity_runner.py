import itertools
import json
import os

from backend.sim.scenario_loader import load_scenario
from backend.sim.digital_twin import run_simulation
from backend.sim.batch_runner import summarize_results

def run_sensitivity(sweep_file):
    with open(sweep_file) as f:
        sweep_def = json.load(f)

    base_scenario = load_scenario(sweep_def["scenario_name"])
    sweep_params = sweep_def["sweep"]

    # Build parameter grid
    keys = list(sweep_params.keys())
    values = [sweep_params[k] for k in keys]
    grid = itertools.product(*values)

    results = []

    for combo in grid:
        # Build modified scenario
        scenario = json.loads(json.dumps(base_scenario))  # deep copy

        for k, v in zip(keys, combo):
            if k in ["kp", "ki"]:
                scenario["servo_adjustments"][k] = v
            elif k == "interference_severity":
                scenario["perturbations"]["interference"]["severity"] = v
            elif k == "outage_duration":
                scenario["perturbations"]["gnss_outage"]["duration"] = v

        # Load samples
        base_day = scenario["base_day"]
        path = f"/opt/ptp-data/live/{base_day}/gnss_samples.json"
        if not os.path.exists(path):
            continue

        with open(path) as f:
            samples = json.load(f)

        # Run simulation
        sim_results = run_simulation(samples, scenario)
        summary = summarize_results(sim_results)

        results.append({
            "parameters": dict(zip(keys, combo)),
            "summary": summary
        })

    return results
