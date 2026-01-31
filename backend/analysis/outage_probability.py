import math

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def compute_outage_probability(f):
    """
    f: outage feature vector
    """

    # Weighted sum of risk factors
    x = 0
    x += (50 - f["forecast_health"]) * 0.05
    x += (50 - f["aging_health"]) * 0.03
    x += f["interference_level"] * 0.4
    x += f["environment_shift"] * 1.2
    x += f["timing_predicted_error"] * 0.002
    x += f["recent_outages"] * 0.5

    # Convert to probability
    p = sigmoid(x)

    return float(min(1.0, max(0.0, p)))
