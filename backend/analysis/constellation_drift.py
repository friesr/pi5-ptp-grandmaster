import numpy as np

def compute_daily_stats(rows):
    """
    rows: list of GNSS entries for a single day
      - constellation
      - snr
    Returns:
      { "GPS": {avg, median, var}, "GAL": {...}, ... }
    """

    constellations = {}

    for r in rows:
        c = r["constellation"]
        constellations.setdefault(c, []).append(r["snr"])

    out = {}
    for c, snrs in constellations.items():
        arr = np.array(snrs)
        out[c] = {
            "avg": float(arr.mean()),
            "median": float(np.median(arr)),
            "var": float(arr.var())
        }

    return out


def compute_drift(history):
    """
    history: list of daily stats in chronological order:
      [
        {"GPS": {avg, median, var}, "GAL": {...}},
        {"GPS": {...}}, ...
      ]

    Returns:
      drift slopes per constellation (dB/day)
    """

    drift = {}

    # Collect per-constellation time series
    series = {}
    for day_stats in history:
        for c, stats in day_stats.items():
            series.setdefault(c, []).append(stats["avg"])

    # Compute slope via simple linear regression
    for c, values in series.items():
        if len(values) < 2:
            drift[c] = 0
            continue

        x = np.arange(len(values))
        y = np.array(values)

        # slope = covariance(x,y) / variance(x)
        slope = np.cov(x, y)[0, 1] / np.var(x)
        drift[c] = float(slope)

    return drift
