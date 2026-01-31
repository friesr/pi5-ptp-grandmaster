#!/bin/bash

LOG_DIR="/opt/ptp-data/live"
ARCHIVE="/opt/ptp-data/archive"

find "$LOG_DIR" -type f -mtime +1 -name "*.json" -exec gzip {} \;

find "$LOG_DIR" -type f -mtime +7 -name "*.json.gz" -exec mv {} "$ARCHIVE" \;

find "$ARCHIVE" -type f -mtime +90 -delete
