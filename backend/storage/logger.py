import os
import csv
import time
from datetime import datetime

def ensure_day_folder(base="/opt/ptp-data/live"):
    day = datetime.utcnow().strftime("%Y-%m-%d")
    path = os.path.join(base, day)
    os.makedirs(path, exist_ok=True)
    return path

def append_row(path, filename, row):
    full = os.path.join(path, filename)
    exists = os.path.exists(full)

    with open(full, "a", newline="") as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(row.keys())
        writer.writerow(row.values())

def log_ptp(ptp):
    path = ensure_day_folder()
    append_row(path, "ptp.csv", {
        "timestamp": ptp["timestamp"],
        "offset_ns": ptp["offset_ns"],
        "gm_present": ptp["gm_present"]
    })

def log_ntp(ntp):
    path = ensure_day_folder()
    append_row(path, "ntp.csv", {
        "timestamp": ntp["timestamp"],
        "offset_ms": ntp["offset_ms"],
        "delay_ms": ntp["delay_ms"]
    })

def log_gnss(gnss):
    path = ensure_day_folder()
    append_row(path, "gnss.csv", {
        "timestamp": gnss["timestamp"],
        "visible": gnss["visible"],
        "used": gnss["used"]
    })

def log_system(system):
    path = ensure_day_folder()
    append_row(path, "system.csv", {
        "timestamp": system["timestamp"],
        "cpu_temp_c": system["cpu_temp_c"],
        "cpu_load_1m": system["cpu_load"][0],
        "memory_percent": system["memory"]
    })
