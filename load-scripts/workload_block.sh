#!/bin/bash

for i in {1..3}; do
  /opt/load-scripts/cpu.sh &
  /opt/load-scripts/ram.sh &
  sleep $((240 + RANDOM % 180))  # 4–7 minutes
done