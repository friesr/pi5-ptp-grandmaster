#!/bin/bash
set -e

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

echo "Installing systemd service..."
cp dashboard.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable dashboard.service

echo "Install complete."
