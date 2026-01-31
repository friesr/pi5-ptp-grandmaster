#!/bin/bash

set -e

echo "Updating system packages..."
apt update
apt upgrade -y

echo "Installing required packages..."
apt install -y \
    python3 python3-pip python3-venv \
    gpsd gpsd-clients python3-gps \
    linuxptp pps-tools ethtool \
    nfs-common git curl

echo "Installing Python dependencies..."
pip3 install flask numpy pandas plotly openpyxl psutil python-dateutil

echo "Creating data directories..."
mkdir -p /opt/ptp-data/live
mkdir -p /opt/ptp-data/archive
mkdir -p /opt/ptp-data/live
mkdir -p /opt/ptp-data/archive

echo "Install complete."
