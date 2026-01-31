import random
import json
import os

from backend.sim.scenario_loader import load_scenario
from backend.sim.digital_twin import run_simulation
from backend.sim.batch_runner import summarize_results

def random_value(base, scale=1.0):
    return base + (random.random() - 0.5) * scale

def mutate(scenario, rate):
    p = scenario["perturbations"]

    if random.random() < rate:
        p["gnss_outage"]["duration"] = max(0, p["gnss_outage"]["duration"] + random_value(0, 300))

    if random.random() < rate:
        p["interference"]["severity"] = max(0, p["interference"]["severity"] + random_value(0, 1.0))

    if random.random() < rate:
        p["spoofing"]["duration"] = max(0, p["spoofing"]["duration"] + random_value(0, 200))

    if random.random() < rate:
        p["multipath_boost"]["factor"] = max(1.0, p["multipath_boost"]["factor"] + random_value(0, 0.5))

    if random.random() < rate:
        p["constellation_failure"]["duration"] = max(0, p["constellation_failure"]["duration"] + random_value(0, 300))

    return scenario

def crossover(a, b):
    child = json.loads(json.dumps(a))

    pa = a["perturbations"]
    pb = b["perturbations"]
    pc = child["perturbations"]

    for key in pc:
        if random.random() < 0.5:
            pc[key] = json.loads(json.dumps(pa[key]))
        else:
            pc[key] = json.loads(json.dumps(pb[key]))

    return child

def fitness(results, objective):
    summary = summarize_results(results)

    if objective == "maximize_rms_error":
        return summary["rms_error"]
    if objective == "maximize_max_error":
        return summary["max_error"]

    return summary["rms_error"]
