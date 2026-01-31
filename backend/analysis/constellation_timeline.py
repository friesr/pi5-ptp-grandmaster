def build_constellation_timeline(rows):
    """
    rows: list of GNSS log entries with:
      - timestamp
      - constellation
      - used (bool)
    """

    # Structure:
    # { "GPS": [ {start, end}, ... ], "GAL": [...], ... }
    timelines = {}

    # Track active intervals per constellation
    active = {}

    for r in rows:
        ts = r["timestamp"]
        c = r["constellation"]
        used = r["used"]

        if c not in timelines:
            timelines[c] = []
        if c not in active:
            active[c] = None

        if used:
            if active[c] is None:
                active[c] = {"start": ts, "end": ts}
            else:
                active[c]["end"] = ts
        else:
            if active[c] is not None:
                timelines[c].append(active[c])
                active[c] = None

    # Close any open intervals
    for c in active:
        if active[c] is not None:
            timelines[c].append(active[c])

    return timelines
