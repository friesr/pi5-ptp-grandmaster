def detect_interference(rows, ptp_events):
    """
    rows: GNSS entries with:
      - timestamp
      - snr
      - multipath
      - state
      - geometry_score

    ptp_events: parsed PTP events

    Returns:
      list of interference events with:
        - timestamp
        - type (jamming/spoofing/noise)
        - severity
        - indicators
    """

    events = []

    for r in rows:
        ts = r["timestamp"]
        snr = r["snr"]
        mp = r["multipath"]
        state = r["state"]
        geom = r["geometry_score"]

        # Jamming: SNR collapse + geometry collapse
        if snr < 5 and geom < 20:
            events.append({
                "timestamp": ts,
                "type": "jamming",
                "severity": "high",
                "indicators": {
                    "snr": snr,
                    "geometry": geom,
                    "multipath": mp,
                    "state": state
                }
            })
            continue

        # Spoofing: high SNR but bad geometry
        if snr > 30 and geom < 20:
            events.append({
                "timestamp": ts,
                "type": "spoofing",
                "severity": "medium",
                "indicators": {
                    "snr": snr,
                    "geometry": geom,
                    "multipath": mp,
                    "state": state
                }
            })
            continue

        # RF noise: SNR sag + multipath
