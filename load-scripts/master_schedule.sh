#!/bin/bash

DAY=$(date +%u)  # 1 = Monday, 7 = Sunday
HOUR=$(date +%H) # 00–23

echo "$(date) – [SCHEDULE] Day: $DAY, Hour: $HOUR" >> /var/log/workload.log

# Monday - Friday (1-5)
if [ "$DAY" -ge 1 ] && [ "$DAY" -le 5 ]; then
  if [ "$HOUR" -ge 9 ] && [ "$HOUR" -le 17 ]; then
    /opt/load-scripts/workload_block.sh &
  fi

  if [ "$HOUR" -eq 23 ]; then
    if [ $((RANDOM % 10)) -lt 8 ]; then
      /opt/load-scripts/io.sh &
    fi
  fi
fi

# Saturday (6)
if [ "$DAY" -eq 6" ]; then
  if [ "$HOUR" -eq 23 ] && [ $((RANDOM % 10)) -lt 5 ]; then
    /opt/load-scripts/io.sh &
  fi
fi

# Sunday (7)
if [ "$DAY" -eq 7" ]; then
  if [ "$HOUR" -eq 2 ] && [ $((RANDOM % 10)) -lt 7 ]; then
    /opt/load-scripts/io.sh &
  fi
fi