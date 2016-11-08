#!/bin/bash

while true; do
  if [ -f /var/run/rotacaster.pid ]; then
    ps up `cat /var/run/rotacaster.pid ` >/dev/null
    if [ $? != 0 ]; then
      # Program has crashed
      echo 0 > /tmp/pwm/0B/enable
      echo 0 > /tmp/pwm/1A/enable
      echo 0 > /tmp/pwm/2A/enable
    fi
  fi
  sleep 0.5
done
