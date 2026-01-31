import os, json

SCENARIO_DIR = "/opt/ptp-data/scenarios"

def list_scenarios():
    return [f for f in os.listdir(SCENARIO_DIR) if f.endswith(".json")]

def load_scenario(name):
    path = os.path.join(SCENARIO_DIR, name)
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)
