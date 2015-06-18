#!/bin/sh

while true; do
  if [ -f /var/run/rotacaster.pid ]; then
    ps up `cat /var/run/rotacaster.pid ` >/dev/null
    if [ $? != 0 ]; then
      # Program has crashed
      echo 0 > /sys/devices/ocp.3/pwm_test_P9_29/duty
      echo 0 > /sys/devices/ocp.3/pwm_test_P8_36/duty
      echo 0 > /sys/devices/ocp.3/pwm_test_P8_45/duty
    fi
  fi
  sleep 0.5
done
