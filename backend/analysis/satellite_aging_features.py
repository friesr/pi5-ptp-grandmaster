def extract_aging_features(history):
    """
    history: list of daily summaries
    Each summary contains:
      - prn_stats: { PRN -> { snr_avg, multipath_avg, geometry_avg, clock_stability, anomaly_count } }
    """

    prn_data = {}

    for day in history:
        stats = day.get("prn_stats", {})
        for prn, s in stats.items():
            if prn not in prn_data:
                prn_data[prn] = {
                    "snr": [],
                    "multipath": [],
                    "geometry": [],
                    "clock": [],
                    "anomalies": []
                }

            prn_data[prn]["snr"].append(s["snr_avg"])
            prn_data[prn]["multipath"].append(s["multipath_avg"])
            prn_data[prn]["geometry"].append(s["geometry_avg"])
            prn_data[prn]["clock"].append(s["clock_stability"])
            prn_data[prn]["anomalies"].append(s["anomaly_count"])

    return prn_data
