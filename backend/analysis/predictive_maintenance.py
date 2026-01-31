import numpy as np

def linear_trend(values):
    """
    values: list of daily metrics
    Returns slope (per day)
    """
    if len(values) < 2:
        return 0

    x = np.arange(len(values))
    y = np.array(values)

    slope = np.cov(x, y)[0, 1] / np.var(x)
    return float(slope)


def predict_failure_days(current_value, slope, threshold):
    """
    Predict days until metric crosses a failure threshold.
    slope < 0 means degrading.
    """
    if slope >= 0:
        return None  # not degrading

    days = (current_value - threshold) / abs(slope)
    return max(0, days)


def build_predictive_maintenance(history):
    """
    history: list of daily summaries with:
      - avg_snr
      - avg_multipath
      - prn_health_avg
      - interference_count
      - geometry_score
      - env_deviation
    """

    # Extract time series
    snr_series = [h["avg_snr"] for h in history]
    mp_series = [h["avg_multipath"] for h in history]
    prn_series = [h["prn_health_avg"] for h in history]
    inter_series = [h["interference_count"] for h in history]
    geom_series = [h["geometry_score"] for h in history]
    env_series = [h["env_deviation"] for h in history]

    # Compute slopes
    snr_slope = linear_trend(snr_series)
    mp_slope = linear_trend(mp_series)
    prn_slope = linear_trend(prn_series)
    inter_slope
