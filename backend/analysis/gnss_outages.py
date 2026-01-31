def detect_outages(rows):
    """
    rows: list of dicts with:
      - timestamp
      - used_count
      - visible_count

    Outage definition: used_count == 0
    """

    outages = []
    current = None

    for r in rows:
        ts = r["timestamp"]
        used = r["used_count"]
        visible = r["visible_count"]

        is_outage = (used == 0)

        if is_outage:
            if current is None:
                current = {
                    "start": ts,
                    "end": ts,
                    "visible_at_start": visible
                }
            else:
                current["end"] = ts
        else:
            if current is not None:
                outages.append(current)
                current = None

    if current is not None:
        outages.append(current)

    for o in outages:
        o["duration_sec"] = o["end"] - o["start"]

    return outages
