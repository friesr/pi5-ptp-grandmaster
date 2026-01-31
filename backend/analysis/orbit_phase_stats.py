import numpy as np
from backend.analysis.orbit_phase import classify_phase

def build_orbit_phase_stats(samples):
    """
    samples: list of GNSS samples with:
      - prn
      - elevation_deg
      - rate_el
      - snr
      - multipath
      - timing_corr
      - eclipse flags
    """

    prn_stats = {}

    for s in samples:
        prn = s["prn"]
        phase = classify_phase(s)

        if prn not in prn_stats:
            prn_stats[prn] = {}

        if phase not in prn_stats[prn]:
            prn_stats[prn][phase] = {
                "snr": [],
                "multipath": [],
                "timing_corr": []
            }

        prn_stats[prn][phase]["snr"].append(s["snr"])
        prn_stats[prn][phase]["multipath"].append(s["multipath"])
        prn_stats[prn][phase]["timing_corr"].append(s["timing_corr"])

    # Compute averages
    results = {}

    for prn, phases in prn_stats.items():
        results[prn] = {}
        for phase, vals in phases.items():
            results[prn][phase] = {
                "snr_avg": float(np.mean(vals["snr"])),
                "multipath_avg": float(np.mean(vals["multipath"])),
                "timing_corr_avg": float(np.mean(vals["timing_corr"]))
            }

    return results
