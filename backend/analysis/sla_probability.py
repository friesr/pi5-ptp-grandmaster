import math

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def compute_sla_probability(f):
    """
    f: SLA feature vector
    """

    x = 0
    x += f["outage_probability"] * 3.0
    x += f["timing_predicted_error"] * 0.003
    x += f["interference_level"] * 0.5
    x += f["environment_shift"] * 1.0
    x += (50 - f["constellation_health"]) * 0.04
    x += (50 - f["aging_health"]) * 0.03
    x += f["recent_sla_violations"] * 0.5

    p = sigmoid(x)
    return float(min(1.0, max(0.0, p)))
