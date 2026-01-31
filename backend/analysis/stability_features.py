def build_stability_features(history):
    """
    history: list of daily summaries
    Returns:
      X: feature matrix
      y: next-day timing error
    """

    X = []
    y = []

    for i in range(len(history) - 1):
        h = history[i]
        next_h = history[i + 1]

        X.append([
            h["timing_error_avg"],
            h["timing_confidence"],
            h["geometry_score"],
            h["avg_snr"],
            h["avg_multipath"],
            h["prn_health_avg"],
            h["interference_count"],
            h["env_deviation"],
            h["receiver_health_score"]
        ])

        y.append(next_h["timing_error_avg"])

    return X, y
