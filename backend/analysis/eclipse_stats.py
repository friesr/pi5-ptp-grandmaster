import numpy as np
from backend.analysis.eclipse_predictor import predict_eclipse

def build_eclipse_stats(samples):
    """
    samples: list of GNSS samples with at least:
      - prn
      - snr
      - multipath
      - timing_corr
      - sat_el / elevation_deg
      - sun_el
      - optional earth_shadow_flag
    Returns:
      dict[prn] -> eclipse behavior stats
    """

    prn_stats = {}

    for s in samples:
        prn = s["prn"]
        in_eclipse = predict_eclipse(s)

        if prn not in prn_stats:
            prn_stats[prn] = {
                "eclipse": {"snr": [], "multipath": [], "timing_corr": []},
                "normal":  {"snr": [], "multipath": [], "timing_corr": []}
            }

        bucket = "eclipse" if in_eclipse else "normal"

        prn_stats[prn][bucket]["snr"].append(s["snr"])
        prn_stats[prn][bucket]["multipath"].append(s["multipath"])
        prn_stats[prn][bucket]["timing_corr"].append(s["timing_corr"])

    results = {}

    for prn, d in prn_stats.items():
        normal_snr = d["normal"]["snr"]
        eclipse_snr = d["eclipse"]["snr"]
        normal_mp = d["normal"]["multipath"]
        eclipse_mp = d["eclipse"]["multipath"]
        normal_tc = d["normal"]["timing_corr"]
        eclipse_tc = d["eclipse"]["timing_corr"]

        if not normal_snr:
            # No baseline, skip
            continue

        snr_drop = 0.0
        mp_change = 0.0
        tc_change = 0.0

        if eclipse_snr:
            snr_drop = float(np.mean(normal_snr) - np.mean(eclipse_snr))
        if eclipse_mp:
            mp_change = float(np.mean(eclipse_mp) - np.mean(normal_mp))
        if eclipse_tc:
            tc_change = float(np.mean(eclipse_tc) - np.mean(normal_tc))

        results[prn] = {
            "snr_drop": snr_drop,
            "multipath_change": mp_change,
            "timing_corr_change": tc_change,
            "eclipse_samples": len(eclipse_snr),
            "normal_samples": len(normal_snr)
        }

    return results
