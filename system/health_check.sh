#!/bin/bash

OUTPUT="/opt/ptp-data/live/system_health.json"

check_service() {
    systemctl is-active --quiet "$1"
    echo "\"$1\": \"$?\","
}

check_mount() {
    mountpoint -q "$1"
    echo "\"nas_mounted\": \"$?\","
}

check_disk() {
    df -h / | awk 'NR==2 {print "\"disk_free\": \"" $4 "\","}'
}

check_gnss() {
    if gpspipe -w -n 10 2>/dev/null | grep -q '"mode":3'; then
        echo "\"gnss_lock\": \"1\","
    else
        echo "\"gnss_lock\": \"0\","
    fi
}

{
echo "{"
check_service "ptp4l.service"
check_service "phc2sys.service"
check_service "logger.service"
check_service "dashboard.service"
check_mount "/mnt/nas"
check_disk
check_gnss
echo "\"timestamp\": \"$(date -Iseconds)\""
echo "}"
} > "$OUTPUT"
