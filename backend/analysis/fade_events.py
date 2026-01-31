def detect_fade_events(rows, snr_threshold=10):
    """
    rows: list of GNSS log entries with:
      - timestamp
      - prn
      - snr
      - used (bool)

    Detects:
      - fade-in: SNR rises above threshold or used becomes True
      - fade-out: SNR drops below threshold or used becomes False
    """

    events = []
    last_state = {}  # prn -> "visible" or "lost"

    for r in rows:
        ts = r["timestamp"]
        prn = r["prn"]
        snr = r["snr"]
        used = r["used"]

        visible = (snr > snr_threshold) or used

        if prn not in last_state:
            last_state[prn] = visible
            continue

        prev = last_state[prn]

        if visible and not prev:
            events.append({
                "timestamp": ts,
                "prn": prn,
                "type": "fade_in",
                "snr": snr
            })

        if not visible and prev:
            events.append({
                "timestamp": ts,
                "prn": prn,
                "type": "fade_out",
                "snr": snr
            })

        last_state[prn] = visible

    return events
