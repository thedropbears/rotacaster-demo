#!/bin/bash

mkdir /tmp/pwm

sleep 10 # give the system time to get the pwm channels up

# Motor A - P9.29, PWM channel B
config-pin P9.29 pwm
echo 1 > /sys/devices/platform/ocp/*.epwmss/48300200.pwm/pwm/pwmchip*/export
ln -s /sys/devices/platform/ocp/*.epwmss/48300200.pwm/pwm/pwmchip*/pwm1 /tmp/pwm/0B

# Motor B - P8.36, PWM channel a
config-pin P8.36 pwm
echo 0 > /sys/devices/platform/ocp/*.epwmss/48302200.pwm/pwm/pwmchip*/export
ln -s /sys/devices/platform/ocp/*.epwmss/48302200.pwm/pwm/pwmchip*/pwm0 /tmp/pwm/1A

# Motor C - P8.45, PWM channel A
config-pin P8.45 pwm
echo 0 > /sys/devices/platform/ocp/*.epwmss/48304200.pwm/pwm/pwmchip*/export
ln -s /sys/devices/platform/ocp/*.epwmss/48304200.pwm/pwm/pwmchip*/pwm0 /tmp/pwm/2A

cd /root/rotacaster-demo
python rotacaster.py &
./rota-watchdog.sh &

