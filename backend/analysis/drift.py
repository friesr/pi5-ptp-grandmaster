import numpy as np

def compute_drift_model(timestamps, offsets_ns):
    """
    timestamps: list of UNIX timestamps
    offsets_ns: list of PTP offsets in nanoseconds
    """

    if len(timestamps) < 10:
        return None

    # Convert to numpy arrays
    t = np.array(timestamps, dtype=float)
    y = np.array(offsets_ns, dtype=float)

    # Normalize time to start at zero
    t0 = t[0]
    t = t - t0

    # Linear regression: y = a*t + b
    A = np.vstack([t, np.ones(len(t))]).T
    slope, intercept = np.linalg.lstsq(A, y, rcond=None)[0]

    # Predict future offsets
    future_times = t[-1] + np.array([60, 300, 600, 3600])  # 1m, 5m, 10m, 1h
    predictions = intercept + slope * future_times

    return {
        "slope_ns_per_sec": slope,
        "intercept_ns": intercept,
        "future_times_sec": future_times.tolist(),
        "future_predictions_ns": predictions.tolist()
    }
