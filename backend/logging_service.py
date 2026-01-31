import time
from backend.sampler.gnss_sampler import sample_gnss
from backend.sampler.ntp_sampler import sample_ntp
from backend.sampler.ptp_sampler import sample_ptp
from backend.sampler.system_sampler import sample_system
from backend.storage.logger import (
    log_ptp, log_ntp, log_gnss, log_system
)
from backend.storage.archive import archive_old_files
from backend.config.manager import load_config

def run_logging_loop():
    while True:
        cfg = load_config()
        interval = cfg.get("refresh_rate_ms", 10000) / 1000.0

        gnss = sample_gnss()
        ntp = sample_ntp()
        ptp = sample_ptp()
        system = sample_system()

        log_gnss(gnss)
        log_ntp(ntp)
        log_ptp(ptp)
        log_system(system)

        archive_old_files()

        time.sleep(interval)
