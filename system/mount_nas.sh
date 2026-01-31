#!/bin/bash

CONFIG="/opt/pi5-ptp-grandmaster/system/nas.conf"

enabled=$(grep enabled $CONFIG | awk -F= '{print $2}' | tr -d ' ')
server=$(grep server $CONFIG | awk -F= '{print $2}' | tr -d ' ')
share=$(grep share $CONFIG | awk -F= '{print $2}' | tr -d ' ')
mount_point=$(grep mount_point $CONFIG | awk -F= '{print $2}' | tr -d ' ')
type=$(grep type $CONFIG | awk -F= '{print $2}' | tr -d ' ')
options=$(grep options $CONFIG | awk -F= '{print $2}' | tr -d ' ')

if [ "$enabled" != "true" ]; then
    echo "NAS mount disabled"
    exit 0
fi

mkdir -p $mount_point

echo "Mounting NAS: $server:$share → $mount_point"

mount -t $type -o $options $server:$share $mount_point
