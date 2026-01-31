import random
import time

def sample_gnss():
    # Simulated GNSS data until hardware is online
    satellites = []
    visible = random.randint(5, 12)
    used = random.randint(3, visible)

    for i in range(visible):
        satellites.append({
            "prn": i + 1,
            "snr": random.randint(20, 45),
            "elevation": random.randint(5, 85),
            "azimuth": random.randint(0, 359),
            "used": i < used
        })

    return {
        "timestamp": time.time(),
        "visible": visible,
        "used": used,
        "satellites": satellites
    }
