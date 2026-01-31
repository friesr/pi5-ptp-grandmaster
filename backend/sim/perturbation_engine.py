def apply_perturbations(sample, scenario):
    t = sample["timestamp"]
    p = scenario.get("perturbations", {})

    # GNSS outage
    if "gnss_outage" in p:
        s = p["gnss_outage"]
        if s["start"] <= t <= s["start"] + s["duration"]:
            sample["snr"] = 0
            sample["tracking"] = False

    # Interference
    if "interference" in p:
        s = p["interference"]
        if s["start"] <= t <= s["start"] + s["duration"]:
            sample["snr"] *= max(0, 1 - s["severity"] * 0.3)

    # Spoofing
    if "spoofing" in p:
        s = p["spoofing"]
        if s["start"] <= t <= s["start"] + s["duration"]:
            sample["pseudorange_residual"] += 50
            sample["doppler_residual"] += 5

    # Multipath boost
    if "multipath_boost" in p:
        sample["multipath"] *= p["multipath_boost"]["factor"]

    # Constellation failure
    if "constellation_failure" in p:
        s = p["constellation_failure"]
        if sample["constellation"] == s["constellation"]:
            if s["start"] <= t <= s["start"] + s["duration"]:
                sample["snr"] = 0
                sample["tracking"] = False

    return sample
