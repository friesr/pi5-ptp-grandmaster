#!/bin/bash
set -e

echo "=== GNSS Timing Observatory Installer ==="

# Ensure script is run as root
if [ "$EUID" -ne 0 ]; then
    echo "ERROR: Please run as root."
    exit 1
fi

# Check internet connectivity
echo "Checking internet connectivity..."
if ! ping -c1 deb.debian.org >/dev/null 2>&1; then
    echo "ERROR: No internet connection detected."
    exit 1
fi

echo "Updating system packages..."
apt update
apt upgrade -y

echo "Installing required system packages..."
apt install -y \
    python3 python3-pip python3-venv \
    gpsd gpsd-clients python3-gps \
    linuxptp pps-tools ethtool \
    nfs-common git curl \
    libatlas-base-dev liblapack-dev gfortran

echo "Installing Python dependencies..."
pip3 install \
    flask numpy pandas plotly openpyxl psutil python-dateutil \
    scipy scikit-learn joblib tqdm Flask-Caching

echo "Creating data directories..."
mkdir -p /opt/ptp-data/live
mkdir -p /opt/ptp-data/archive
mkdir -p /opt/ptp-data/scenarios/library
mkdir -p /opt/ptp-data/scenarios/more_features
mkdir -p /opt/ptp-data/reports
mkdir -p /opt/ptp-data/exports

echo "Setting permissions..."
chmod -R 755 /opt/ptp-data

echo "Installing systemd services..."
SYSTEM_DIR="/opt/pi5-ptp-grandmaster/system"

SERVICES=(
    dashboard.service
    logger.service
    ptp4l.service
    phc2sys.service
    ptp-status.service
    system_check.service
    system_check.timer
)

for svc in "${SERVICES[@]}"; do
    if [ -f "$SYSTEM_DIR/$svc" ]; then
        cp "$SYSTEM_DIR/$svc" /etc/systemd/system/
        echo "Installed $svc"
    else
        echo "WARNING: $svc not found in system directory"
    fi
done

echo "Reloading systemd..."
systemctl daemon-reload

echo "Enabling services..."
systemctl enable dashboard.service
systemctl enable logger.service
systemctl enable ptp4l.service
systemctl enable phc2sys.service
systemctl enable ptp-status.service
systemctl enable system_check.service
systemctl enable system_check.timer

echo "Install complete."
echo "Reboot recommended."
