import os
import subprocess

def nas_is_mounted(path="/mnt/nas"):
    return os.path.ismount(path)

def nas_ping(server):
    try:
        subprocess.check_output(["ping", "-c", "1", "-W", "1", server])
        return True
    except:
        return False

def nas_free_space_gb(path="/mnt/nas"):
    if not nas_is_mounted(path):
        return None

    stat = os.statvfs(path)
    free = stat.f_bavail * stat.f_frsize
    return free / (1024**3)
