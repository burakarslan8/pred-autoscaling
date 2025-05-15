#!/bin/bash

RAM_MB=$((128 + RANDOM % 384))       # 128–640 MB
DURATION=$((120 + RANDOM % 180))
DELAY=$((RANDOM % 180))

sleep $DELAY

echo "$(date) - [RAM] load starting: ${RAM_MB} MB for $DURATION sec (delay $DELAY s)" >> /var/log/workload.log
stress --vm 1 --vm-bytes ${RAM_MB}M --timeout $DURATION