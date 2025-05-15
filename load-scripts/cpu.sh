#!/bin/bash

# Randomize CPU load
CPU_LOAD=$((1 + RANDOM % 2))        # 1–3 core
DURATION=$((180 + RANDOM % 240))    # 1–5 minutes
DELAY=$((RANDOM % 180))            # Max 5 m delay

sleep $DELAY

echo "$(date) - [CPU] load starting: $CPU_LOAD core(s) for $DURATION sec (delay $DELAY s)" >> /var/log/workload.log
stress --cpu $CPU_LOAD --timeout $DURATION