def compute_prn_lifetimes(rows):
    """
    rows: list of GNSS log entries for a day
    Each row contains: timestamp, prn, used, visible
    """

    lifetimes = {}

    for r in rows:
        prn = r["prn"]
        if prn not in lifetimes:
            lifetimes[prn] = {
                "visible_start": None,
                "visible_end": None,
                "used_start": None,
                "used_end": None,
                "visible_total": 0,
                "used_total": 0,
                "last_ts": None
            }

        entry = lifetimes[prn]
        ts = r["timestamp"]

        # Visible tracking
        if r["visible"]:
            if entry["visible_start"] is None:
                entry["visible_start"] = ts
            entry["visible_end"] = ts
        else:
            if entry["visible_start"] is not None:
                entry["visible_total"] += entry["visible_end"] - entry["visible_start"]
                entry["visible_start"] = None

        # Used tracking
        if r["used"]:
            if entry["used_start"] is None:
                entry["used_start"] = ts
            entry["used_end"] = ts
        else:
            if entry["used_start"] is not None:
                entry["used_total"] += entry["used_end"] - entry["used_start"]
                entry["used_start"] = None

        entry["last_ts"] = ts

    # Close open intervals
    for prn, entry in lifetimes.items():
        if entry["visible_start"] is not None:
            entry["visible_total"] += entry["last_ts"] - entry["visible_start"]
        if entry["used_start"] is not None:
            entry["used_total"] += entry["last_ts"] - entry["used_start"]

    # Convert seconds to minutes
    for prn, entry in lifetimes.items():
        entry["visible_minutes"] = entry["visible_total"] / 60
        entry["used_minutes"] = entry["used_total"] / 60

    return lifetimes
