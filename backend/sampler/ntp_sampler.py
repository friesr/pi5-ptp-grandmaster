import subprocess
import time
import random

def sample_ntp():
    try:
        out = subprocess.check_output(["chronyc", "tracking"], text=True)
        offset = None
        delay = None

        for line in out.splitlines():
            if "Last offset" in line:
                offset = float(line.split(":")[1].split()[0]) * 1000  # ms
            if "Root delay" in line:
                delay = float(line.split(":")[1].split()[0]) * 1000  # ms

        if offset is None:
            raise Exception("chrony output incomplete")

        return {
            "timestamp": time.time(),
            "server": "chrony",
            "offset_ms": round(offset, 3),
            "delay_ms": round(delay, 3) if delay else None
        }

    except Exception:
        # fallback simulation
        return {
            "timestamp": time.time(),
            "server": "simulated",
            "offset_ms": round(random.uniform(-2.0, 2.0), 3),
            "delay_ms": round(random.uniform(5.0, 25.0), 3)
        }
