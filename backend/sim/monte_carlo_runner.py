import json
import os

from backend.sim.scenario_loader import load_scenario
from backend.sim.digital_twin import run_simulation
from backend.sim.batch_runner import summarize_results
from backend.sim.monte_carlo_randomizer import randomize_scenario

def run_monte_carlo(cfg_file):
    with open(cfg_file) as f:
        cfg = json.load(f)

    base = load_scenario(cfg["scenario_name"])
    iterations = cfg["iterations"]
    rand_cfg = cfg["randomization"]

    base_day = base["base_day"]
    path = f"/opt/ptp-data/live/{base_day}/gnss_samples.json"

    with open(path) as f:
        samples = json.load(f)

    results = []

    for i in range(iterations):
        scenario = randomize_scenario(base, rand_cfg)
        sim = run_simulation(samples, scenario)
        summary = summarize_results(sim)

        results.append({
            "iteration": i,
            "summary": summary
        })

    return results
