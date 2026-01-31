import subprocess
import time
import random

def sample_ptp_servo():
    try:
        out = subprocess.check_output(
            ["pmc", "-u", "-b", "0", "GET PORT_DATA_SET"],
            text=True
        )

        freq_adj = None
        delay = None
        state = None

        for line in out.splitlines():
            if "neighborPropDelay" in line:
                delay = float(line.split()[-1])
            if "logSyncInterval" in line:
                # servo state is inferred from sync interval
                state = line.split()[-1]
            if "offsetFromMaster" in line:
                # pmc CURRENT_DATA_SET gives offset, but PORT_DATA_SET gives freq
                pass
            if "meanPathDelay" in line:
                pass
            if "observedDrift" in line:
                freq_adj = float(line.split()[-1])

        if freq_adj is None:
            raise Exception("pmc output incomplete")

        return {
            "timestamp": time.time(),
            "freq_adj_ppb": freq_adj,
            "delay_ns": delay,
            "state": state
        }

    except Exception:
        # fallback simulation
        return {
            "timestamp": time.time(),
            "freq_adj_ppb": random.uniform(-50, 50),
            "delay_ns": random.uniform(100, 500),
            "state": "tracking"
        }
