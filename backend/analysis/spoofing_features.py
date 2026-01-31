def extract_spoofing_features(a, b, constellation_perf, env_dev, timing, interference):
    """
    a, b: receiver A/B daily summaries
    constellation_perf: constellation performance metrics
    env_dev: environment deviation score
    timing: timing metrics (offset, drift, stability)
    interference: interference metrics
    """

    return {
        "timing_divergence": abs(a["timing_error_avg"] - b["timing_error_avg"]),
        "confidence_divergence": abs(a["timing_confidence"] - b["timing_confidence"]),
        "constellation_bias": constellation_perf.get("GPS", {}).get("avg_drift", 0)
                              - constellation_perf.get("GAL", {}).get("avg_drift", 0),
        "environment_shift": env_dev,
        "interference_level": interference.get("severity_avg", 0),
        "timing_stability": timing.get("predicted_timing_error_ns", 0)
    }
