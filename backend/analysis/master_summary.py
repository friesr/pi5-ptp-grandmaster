def build_master_summary(day, components):
    """
    components: dict containing:
      - timing_confidence
      - stability_prediction
      - receiver_health
      - environment_change
      - sla
      - gnss_metrics
      - ptp_metrics
      - predictive_maintenance
      - events
    """

    return {
        "day": day,
        "timing": {
            "confidence": components["timing_confidence"],
            "stability_prediction": components["stability_prediction"],
            "ptp": components["ptp_metrics"],
            "sla": components["sla"]
        },
        "gnss": {
            "metrics": components["gnss_metrics"],
            "receiver_health": components["receiver_health"],
            "environment_change": components["environment_change"]
        },
        "predictive": {
            "maintenance": components["predictive_maintenance"]
        },
        "events": components["events"]
    }
