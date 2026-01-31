import random
import json

def rand_range(spec):
    return spec["min"] + random.random() * (spec["max"] - spec["min"])

def randomize_scenario(base, rand_cfg):
    s = json.loads(json.dumps(base))  # deep copy

    p = s["perturbations"]

    p["gnss_outage"]["start"] = int(rand_range(rand_cfg["outage_start"]))
    p["gnss_outage"]["duration"] = int(rand_range(rand_cfg["outage_duration"]))

    p["interference"]["severity"] = rand_range(rand_cfg["interference_severity"])

    p["spoofing"]["duration"] = int(rand_range(rand_cfg["spoofing_duration"]))

    p["multipath_boost"]["factor"] = rand_range(rand_cfg["multipath_factor"])

    p["constellation_failure"]["duration"] = int(rand_range(rand_cfg["constellation_failure_duration"]))

    s["receiver_health_drop"] = {
        "score": int(rand_range(rand_cfg["receiver_health"]))
    }

    return s
