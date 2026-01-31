#!/bin/bash

CONFIG="/opt/pi5-ptp-grandmaster/system/nas.conf"

# Function to read key=value safely
get_conf() {
    local key="$1"
    grep -E "^$key=" "$CONFIG" | sed -e "s/^$key=//" -e 's/^[ \t]*//;s/[ \t]*$//'
}

enabled=$(get_conf enabled)
server=$(get_conf server)
share=$(get_conf share)
mount_point=$(get_conf mount_point)
type=$(get_conf type)
options=$(get_conf options)

# Exit if disabled
if [ "$enabled" != "true" ]; then
    echo "NAS mount disabled"
    exit 0
fi

# Validate required fields
if [ -z "$server" ] || [ -z "$share" ] || [ -z "$mount_point" ] || [ -z "$type" ]; then
    echo "ERROR: Missing required NAS configuration fields"
    exit 1
fi

# Create mount point
mkdir -p "$mount_point"

# Check if already mounted
if mountpoint -q "$mount_point"; then
    echo "NAS already mounted at $mount_point"
    exit 0
fi

echo "Mounting NAS: $server:$share → $mount_point"

# Attempt mount with error handling
if ! mount -t "$type" -o "$options" "$server:$share" "$mount_point"; then
    echo "ERROR: Failed to mount NAS"
    exit 1
fi

echo "NAS mounted successfully"
exit 0
