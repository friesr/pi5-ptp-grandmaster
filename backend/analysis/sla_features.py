def extract_sla_features(day_summary, outage_prob, timing_pred, interference, env_dev, constellation_forecast, aging):
    """
    day_summary: today's GNSS/PTP summary
    outage_prob: predicted outage probability
    timing_pred: predicted timing error
    interference: interference summary
    env_dev: environment deviation score
    constellation_forecast: forecasted constellation health
    aging: per-PRN aging scores
    """

    # Aggregate constellation forecast
    forecast_avg = sum(v["forecast_health_score"] for v in constellation_forecast.values()) / max(1, len(constellation_forecast))

    # Aggregate aging
    aging_avg = sum(v["aging_score"] for v in aging.values()) / max(1, len(aging))

    return {
        "outage_probability": outage_prob,
        "timing_predicted_error": timing_pred.get("predicted_timing_error_ns", 0),
        "interference_level": interference.get("severity_avg", 0),
        "environment_shift": env_dev,
        "constellation_health": forecast_avg,
        "aging_health": aging_avg,
        "recent_sla_violations": day_summary.get("sla_violations", 0)
    }
