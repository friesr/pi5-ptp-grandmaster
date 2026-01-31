import random
import time

def sample_ptp():
    # Simulated PTP offset in nanoseconds
    offset_ns = random.uniform(-500.0, 500.0)

    return {
        "timestamp": time.time(),
        "offset_ns": round(offset_ns, 1),
        "gm_present": True
    }
