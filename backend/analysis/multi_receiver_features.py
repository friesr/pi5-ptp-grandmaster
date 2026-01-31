def extract_correlation_features(a, b):
    """
    a, b: daily summaries for receiver A and B
    Returns correlation metrics.
    """

    return {
        "snr_diff": abs(a["avg_snr"] - b["avg_snr"]),
        "multipath_diff": abs(a["avg_multipath"] - b["avg_multipath"]),
        "geometry_diff": abs(a["geometry_score"] - b["geometry_score"]),
        "prn_health_diff": abs(a["prn_health_avg"] - b["prn_health_avg"]),
        "interference_diff": abs(a["interference_count"] - b["interference_count"]),
        "timing_error_diff": abs(a["timing_error_avg"] - b["timing_error_avg"]),
        "confidence_diff": abs(a["timing_confidence"] - b["timing_confidence"]),
        "env_dev_diff": abs(a["env_deviation"] - b["env_deviation"])
    }
