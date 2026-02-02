def extract_clock_features(samples):
    """
    samples: list of GNSS samples with:
      - prn
      - pseudorange_residual
      - doppler_residual
      - timing_corr
      - elevation_deg
      - eclipse flags (optional)
    """

    prn_data = {}

    for s in samples:
        prn = s["prn"]

        if prn not in prn_data:
            prn_data[prn] = {
                "pr_res": [],
                "dop_res": [],
                "timing_corr": [],
                "eclipse": [],
                "elevation": []
            }

        prn_data[prn]["pr_res"].append(s["pseudorange_residual"])
        prn_data[prn]["dop_res"].append(s["doppler_residual"])
        prn_data[prn]["timing_corr"].append(s["timing_corr"])
        prn_data[prn]["elevation"].append(s["elevation_deg"])
        prn_data[prn]["eclipse"].append(s.get("earth_shadow_flag", False))

    return prn_data
