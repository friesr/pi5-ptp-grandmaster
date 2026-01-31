# Installation guide

This document describes how to install and run the **GNSS Timing Observatory / PTP Grandmaster Dashboard** on a fresh system (e.g. Raspberry Pi 5).

---

## 1. System requirements

**Hardware:**

- Raspberry Pi 4/5 (or similar ARM/AMD64 Linux host)
- GNSS receiver with PPS output
- Stable network connection

**OS:**

- Debian / Ubuntu / Raspberry Pi OS (systemd-based)

---

## 2. System package installation

Update and upgrade:

```bash
sudo apt update
sudo apt upgrade -y
