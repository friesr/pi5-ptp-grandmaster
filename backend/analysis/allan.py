import numpy as np

def compute_allan_deviation(offsets_ns, tau_values):
    """
    offsets_ns: list of timing offsets in nanoseconds
    tau_values: list of averaging times (in seconds)
    """

    if len(offsets_ns) < 10:
        return {tau: None for tau in tau_values}

    adev_results = {}

    # Convert to numpy array
    x = np.array(offsets_ns, dtype=float)

    for tau in tau_values:
        m = int(tau)  # number of samples per averaging period

        if m < 1 or m * 2 >= len(x):
            adev_results[tau] = None
            continue

        # Compute overlapping Allan deviation
        y = x
        diff = y[2*m:] - 2*y[m:-m] + y[:-2*m]
        adev = np.sqrt(0.5 * np.mean(diff**2)) / (m)
        adev_results[tau] = adev

    return adev_results
