def fuse_confidence_features(
    timing_pred,
    outage_prob,
    sla_prob,
    constellation_forecast,
    aging,
    clock_stats,
    interference,
    env_dev,
    multipath,
    receiver_health,
    spoofing
):
    # Aggregate constellation forecast
    const_avg = sum(v["forecast_health_score"] for v in constellation_forecast.values()) / max(1, len(constellation_forecast))

    # Aggregate aging
    aging_avg = sum(v["aging_score"] for v in aging.values()) / max(1, len(aging))

    # Aggregate clock stability
    clock_avg = sum(v["clock_stability_score"] for v in clock_stats.values()) / max(1, len(clock_stats))

    # Aggregate multipath
    mp_avg = sum(v["severity"] for v in multipath) / max(1, len(multipath))

    return {
        "timing_predicted_error": timing_pred.get("predicted_timing_error_ns", 0),
        "outage_probability": outage_prob,
        "sla_probability": sla_prob,
        "constellation_health": const_avg,
        "aging_health": aging_avg,
        "clock_health": clock_avg,
        "interference_level": interference.get("severity_avg", 0),
        "environment_shift": env_dev,
        "multipath_severity": mp_avg,
        "receiver_health": receiver_health.get("health_score", 100),
        "spoofing_flag": 1 if spoofing.get("classification") != "no_spoofing_detected" else 0
    }
