def compute_timing_confidence2(f):
    score = 100

    # Timing stability
    score -= f["timing_predicted_error"] * 0.1

    # Outage & SLA risk
    score -= f["outage_probability"] * 40
    score -= f["sla_probability"] * 30

    # Constellation & satellite health
    score += (f["constellation_health"] - 50) * 0.2
    score += (f["aging_health"] - 50) * 0.1
    score += (f["clock_health"] - 50) * 0.2

    # RF environment
    score -= f["interference_level"] * 5
    score -= f["environment_shift"] * 20
    score -= f["multipath_severity"] * 10

    # Hardware
    score += (f["receiver_health"] - 70) * 0.1

    # Spoofing
    if f["spoofing_flag"]:
        score -= 25

    return max(0, min(100, score))
