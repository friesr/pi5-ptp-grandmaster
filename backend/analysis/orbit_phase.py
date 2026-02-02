def classify_phase(sample):
    el = sample["elevation_deg"]

    # Simple elevation-based phase classification
    if el < 15:
        return "ascending" if sample["rate_el"] > 0 else "descending"
    if el > 70:
        return "peak"

    # Eclipse detection (requires flags in sample)
    if sample.get("eclipse_entry", False):
        return "eclipse_entry"
    if sample.get("eclipse_exit", False):
        return "eclipse_exit"

    return "mid_arc"
