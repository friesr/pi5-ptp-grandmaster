def classify_spoofing(f):
    """
    f: spoofing feature vector
    """

    # Strong spoofing signature: both receivers diverge together
    if f["timing_divergence"] > 200 and f["confidence_divergence"] < 5:
        return "spoofing_suspected"

    # Meaconing: constellation-wide bias + stable timing error
    if abs(f["constellation_bias"]) > 0.5 and f["timing_stability"] > 100:
        return "meaconing_suspected"

    # Environment anomaly + timing drift
    if f["environment_shift"] > 0.5 and f["timing_stability"] > 150:
        return "environmental_spoofing_possible"

    # Interference + timing pull
    if f["interference_level"] > 2 and f["timing_stability"] > 80:
        return "interference_induced_timing_attack_possible"

    return "no_spoofing_detected"
