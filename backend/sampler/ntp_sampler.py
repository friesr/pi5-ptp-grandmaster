import random
import time

def sample_ntp():
    # Simulated NTP offset and delay
    offset_ms = random.uniform(-2.0, 2.0)
    delay_ms = random.uniform(5.0, 25.0)

    return {
        "timestamp": time.time(),
        "server": "pool.ntp.org",
        "offset_ms": round(offset_ms, 3),
        "delay_ms": round(delay_ms, 3)
    }
