def explain_root_cause(f):
    explanations = []

    # Outage probability
    if f["outage_probability"] > 0.4:
        explanations.append({
            "factor": "High GNSS outage probability",
            "severity": f["outage_probability"],
            "reason": "Forecasted constellation and satellite conditions indicate elevated outage risk."
        })

    # Timing predicted error
    if f["timing_predicted_error"] > 80:
        explanations.append({
            "factor": "Timing instability",
            "severity": f["timing_predicted_error"] / 200,
            "reason": "Predicted timing error exceeds stable operating thresholds."
        })

    # Interference
    if f["interference_level"] > 1.5:
        explanations.append({
            "factor": "RF interference",
            "severity": f["interference_level"] / 5,
            "reason": "Interference levels are high enough to degrade GNSS tracking."
        })

    # Environment shift
    if f["environment_shift"] > 0.3:
        explanations.append({
            "factor": "Environment deviation",
            "severity": f["environment_shift"],
            "reason": "The RF environment has changed significantly compared to baseline."
        })

    # Constellation health
    if f["constellation_health"] < 60:
        explanations.append({
            "factor": "Weak constellation health",
            "severity": (60 - f["constellation_health"]) / 60,
            "reason": "Forecasted constellation performance is below nominal levels."
        })

    # Satellite aging
    if f["aging_health"] < 70:
        explanations.append({
            "factor": "Satellite aging effects",
            "severity": (70 - f["aging_health"]) / 70,
            "reason": "Long-term degradation in satellite performance is contributing to instability."
        })

    # Recent SLA violations
    if f["recent_sla_violations"] > 0:
        explanations.append({
            "factor": "Recent SLA violations",
            "severity": min(1.0, f["recent_sla_violations"] * 0.2),
            "reason": "Recent SLA failures indicate ongoing instability."
        })

    # Sort by severity
    explanations.sort(key=lambda x: -x["severity"])

    return explanations
