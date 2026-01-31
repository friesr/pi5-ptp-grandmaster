import numpy as np

def compute_servo_stability(samples):
    """
    samples: list of dicts with freq_adj_ppb and delay_ns
    Returns a stability score and metrics.
    """

    if len(samples) < 20:
        return None

    freq = np.array([s["freq_adj_ppb"] for s in samples])
    delay = np.array([s["delay_ns"] for s in samples])

    freq_std = np.std(freq)
    delay_std = np.std(delay)

    # Normalize into a 0–100 score
    # Lower variance = higher stability
    freq_score = max(0, 100 - freq_std)
    delay_score = max(0, 100 - delay_std / 10)

    score = (freq_score * 0.6) + (delay_score * 0.4)
    score = max(0, min(100, score))

    if score > 90:
        quality = "excellent"
    elif score > 75:
        quality = "good"
    elif score > 50:
        quality = "fair"
    else:
        quality = "poor"

    return {
        "score": score,
        "quality": quality,
        "freq_std": float(freq_std),
        "delay_std": float(delay_std)
    }
