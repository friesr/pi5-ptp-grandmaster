def infer_receiver_health(drift, prn_health, interference_events):
    """
    drift: constellation drift slopes (dB/day)
    prn_health: per-PRN health scores
    interference_events: list of interference detections

    Returns:
      hardware health classification + indicators
    """

    # Aggregate PRN health
    avg_prn_health = sum(prn_health.values()) / len(prn_health)

    # Drift indicators
    drift_values = list(drift.values())
    avg_drift = sum(drift_values) / len(drift_values)

    # Interference presence
    has_jamming = any(e["type"] == "jamming" for e in interference_events)
    has_noise = any(e["type"] == "rf_noise" for e in interference_events)

    # Classification logic
    issues = []

    # Antenna degradation: slow SNR decline + low PRN health
    if avg_drift < -0.2 and avg_prn_health < 70:
        issues.append("antenna_degradation")

    # Cable loss: slow SNR decline but PRN health still moderate
    if avg_drift < -0.2 and avg_prn_health >= 70:
        issues.append("cable_loss")

    # LNA failure: sudden SNR collapse + no interference
    if avg_drift < -1.0 and not has_jamming and not has_noise:
        issues.append("lna_failure")

    # Receiver instability: PRN health oscillating
    if any(h["multipath_max"] > 0.8 for h in prn_health.values()):
        issues.append("receiver_instability")

    if not issues:
        issues.append("healthy")

    return {
        "avg_prn_health": avg_prn_health,
        "avg_drift": avg_drift,
        "issues": issues
    }
