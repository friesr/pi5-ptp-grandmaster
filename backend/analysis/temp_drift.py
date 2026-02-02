import numpy as np

def compute_temp_drift_model(temps_c, offsets_ns):
    """
    temps_c: list of CPU temperatures
    offsets_ns: list of PTP offsets
    """

    if len(temps_c) < 10 or len(offsets_ns) < 10:
        return None

    t = np.array(temps_c, dtype=float)
    y = np.array(offsets_ns, dtype=float)

    # Linear regression: offset = a * temp + b
    A = np.vstack([t, np.ones(len(t))]).T
    slope, intercept = np.linalg.lstsq(A, y, rcond=None)[0]

    # Predict offsets at key temperatures
    temps_future = np.array([40, 50, 60, 70])
    predictions = intercept + slope * temps_future

    return {
        "slope_ns_per_c": slope,
        "intercept_ns": intercept,
        "temps_c": temps_future.tolist(),
        "predicted_offsets_ns": predictions.tolist()
    }
