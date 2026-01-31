import psutil

def sample_system():
    return {
        "cpu_temp_c": None,  # Pi-specific path added later
        "cpu_load": psutil.getloadavg(),
        "memory": psutil.virtual_memory().percent
    }
