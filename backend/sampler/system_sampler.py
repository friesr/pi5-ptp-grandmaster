import psutil
import time
import random

def sample_system():
    return {
        "timestamp": time.time(),
        "cpu_temp_c": random.uniform(40.0, 65.0),  # placeholder until Pi is online
        "cpu_load": psutil.getloadavg(),
        "memory": psutil.virtual_memory().percent
    }
