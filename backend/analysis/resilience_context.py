def build_resilience_context(root_cause, outage_prob, timing_pred, interference, env_dev, siting, receiver_health):
    return {
        "root_cause": root_cause,
        "outage_probability": outage_prob,
        "timing_predicted_error": timing_pred.get("predicted_timing_error_ns", 0),
        "interference_level": interference.get("severity_avg", 0),
        "environment_shift": env_dev,
        "best_siting": siting[0] if siting else None,
        "receiver_health": receiver_health
    }
