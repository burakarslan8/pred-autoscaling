#!/bin/bash

SIZE_MB=$((50 + RANDOM % 250))     # 100–600 MB
DELAY=$((RANDOM % 180))

sleep $DELAY

echo "$(date) - [I/O] writing $SIZE_MB MB (delay $DELAY s)" >> /var/log/workload.log
dd if=/dev/zero of=/tmp/testfile bs=1M count=$SIZE_MB oflag=dsync
rm -f /tmp/testfile