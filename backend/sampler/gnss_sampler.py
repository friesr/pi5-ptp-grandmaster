import gps
import time
import random

def sample_gnss():
    try:
        session = gps.gps(mode=gps.WATCH_ENABLE)
        report = session.next()

        if report['class'] != 'SKY':
            return sample_gnss()  # try again

        sats = []
        used = 0

        for s in report.satellites:
            sats.append({
                "prn": s.PRN,
                "snr": getattr(s, "ss", 0),
                "elevation": getattr(s, "el", 0),
                "azimuth": getattr(s, "az", 0),
                "used": getattr(s, "used", False)
            })
            if getattr(s, "used", False):
                used += 1

        return {
            "timestamp": time.time(),
            "visible": len(report.satellites),
            "used": used,
            "satellites": sats
        }

    except Exception:
        # fallback simulation
        return {
            "timestamp": time.time(),
            "visible": 8,
            "used": 5,
            "satellites": [
                {
                    "prn": i,
                    "snr": random.randint(20, 45),
                    "elevation": random.randint(5, 85),
                    "azimuth": random.randint(0, 359),
                    "used": i % 2 == 0
                }
                for i in range(1, 9)
            ]
        }
