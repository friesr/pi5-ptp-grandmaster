def extract_constellation_timeseries(history):
    """
    history: list of daily summaries
    Each summary contains:
      - per_constellation: {
            "GPS": {...},
            "GAL": {...},
            "BDS": {...},
            "GLO": {...}
        }
    """

    constellations = ["GPS", "GAL", "BDS", "GLO"]
    data = {c: {"snr": [], "multipath": [], "geometry": [], "timing_corr": []} for c in constellations}

    for day in history:
        per = day.get("per_constellation", {})
        for c in constellations:
            if c not in per:
                continue
            d = per[c]
            data[c]["snr"].append(d["avg_snr"])
            data[c]["multipath"].append(d["avg_multipath"])
            data[c]["geometry"].append(d["geometry_score"])
            data[c]["timing_corr"].append(d["timing_correlation"])

    return data
