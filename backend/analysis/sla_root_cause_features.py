def fuse_root_cause_features(sla_features, outage_features):
    """
    sla_features: dict from SLA predictor
    outage_features: dict from outage predictor
    """

    return {
        "sla_violation_probability": sla_features["sla_violation_probability"],
        "outage_probability": outage_features["outage_probability"],
        "timing_predicted_error": sla_features["features"]["timing_predicted_error"],
        "interference_level": sla_features["features"]["interference_level"],
        "environment_shift": sla_features["features"]["environment_shift"],
        "constellation_health": sla_features["features"]["constellation_health"],
        "aging_health": sla_features["features"]["aging_health"],
        "recent_sla_violations": sla_features["features"]["recent_sla_violations"]
    }
