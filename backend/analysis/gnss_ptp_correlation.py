def correlate_gnss_ptp(gnss_rows, ptp_events, window=5):
    """
    Correlate GNSS anomalies with PTP events.

    window: seconds before/after a PTP event to search for GNSS anomalies.
    """

    correlations = []

    for event in ptp_events:
        ts = event["timestamp"]

        # Find GNSS rows within ±window seconds
        nearby = [
            r for r in gnss_rows
            if abs(r["timestamp"] - ts) <= window
        ]

        if not nearby:
            continue

        # Extract anomaly indicators
        multipath = max(r["multipath"] for r in nearby)
        snr_min = min(r["snr"] for r in nearby)
        fading = any(r.get("state") == "fading" for r in nearby)
        obstructed = any(r.get("state") == "obstructed" for r in nearby)
        lost = any(r.get("state") == "lost" for r in nearby)
        geometry = min(r.get("geometry_score", 100) for r in nearby)

        correlations.append({
            "ptp_event": event,
            "multipath": multipath,
            "snr_min": snr_min,
            "fading": fading,
            "obstructed": obstructed,
            "lost": lost,
            "geometry_score": geometry
        })

    return correlations
