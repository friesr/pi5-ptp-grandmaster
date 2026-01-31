import time

from backend.sampler.gnss_sampler import sample_gnss
from backend.sampler.ntp_sampler import sample_ntp
from backend.sampler.ptp_sampler import sample_ptp
from backend.sampler.system_sampler import sample_system
from backend.sampler.ptp_servo_sampler import sample_ptp_servo

from backend.storage.logger import (
    log_ptp,
    log_ntp,
    log_gnss,
    log_system,
    append_row,
    ensure_day_folder
)

from backend.storage.archive import archive_old_files
from backend.config.manager import load_config


def log_servo():
    """Log PTP servo data into servo.csv."""
    servo = sample_ptp_servo()
    path = ensure_day_folder()

    append_row(path, "servo.csv", {
        "timestamp": servo["timestamp"],
        "freq_adj_ppb": servo["freq_adj_ppb"],
        "delay_ns": servo["delay_ns"],
        "state": servo["state"]
    })


def run_logging_loop():
    """
    Main background logging loop.
    Runs forever under systemd.
    Logs GNSS, NTP, PTP, System, and Servo data.
    Enforces storage limits and archives old files.
    """

    while True:
        cfg = load_config()
        interval = cfg.get("refresh_rate_ms", 10000) / 1000.0

        # Sample all timing sources
        gnss = sample_gnss()
        ntp = sample_ntp()
        ptp = sample_ptp()
        system = sample_system()

        # Log each subsystem
        log_gnss(gnss)
        log_ntp(ntp)
        log_ptp(ptp)
        log_system(system)
        log_servo()

        # Enforce storage limits + archive
        archive_old_files()

        time.sleep(interval)
