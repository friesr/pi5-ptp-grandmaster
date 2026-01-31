#!/bin/bash

echo "Running system bootstrap..."

dirs=(
    /opt/ptp-data/live
    /opt/ptp-data/archive
    /opt/ptp-data/scenarios/library
    /opt/ptp-data/reports
    /opt/ptp-data/exports
)

for d in "${dirs[@]}"; do
    mkdir -p "$d"
done

chmod -R 755 /opt/ptp-data

systemctl enable ptp4l.service
systemctl enable phc2sys.service
systemctl enable logger.service
systemctl enable dashboard.service
systemctl enable system_check.timer

echo "Bootstrap complete."
