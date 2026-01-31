def extract_outage_features(day_summary, constellation_forecast, aging, interference, env_dev, timing_pred):
    """
    day_summary: today's GNSS summary
    constellation_forecast: forecasted constellation health
    aging: per-PRN aging scores
    interference: interference summary
    env_dev: environment deviation score
    timing_pred: predicted timing error
    """

    # Aggregate aging into a constellation-level average
    aging_avg = sum(v["aging_score"] for v in aging.values()) / max(1, len(aging))

    # Forecast health average
    forecast_avg = sum(v["forecast_health_score"] for v in constellation_forecast.values()) / max(1, len(constellation_forecast))

    return {
        "forecast_health": forecast_avg,
        "aging_health": aging_avg,
        "interference_level": interference.get("severity_avg", 0),
        "environment_shift": env_dev,
        "timing_predicted_error": timing_pred.get("predicted_timing_error_ns", 0),
        "recent_outages": day_summary.get("outage_count", 0)
    }
