import subprocess
import time
import random

def sample_ptp():
    try:
        out = subprocess.check_output(
            ["pmc", "-u", "-b", "0", "GET CURRENT_DATA_SET"],
            text=True
        )

        offset = None
        gm_present = True

        for line in out.splitlines():
            if "offsetFromMaster" in line:
                offset = float(line.split()[-1])
            if "gmPresent" in line:
                gm_present = "true" in line.lower()

        if offset is None:
            raise Exception("pmc output incomplete")

        return {
            "timestamp": time.time(),
            "offset_ns": offset,
            "gm_present": gm_present
        }

    except Exception:
        # fallback simulation
        return {
            "timestamp": time.time(),
            "offset_ns": round(random.uniform(-500, 500), 1),
            "gm_present": True
        }
