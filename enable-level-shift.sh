#!/bin/sh

echo 20 > /sys/class/gpio/export

echo 'out' > /sys/class/gpio/gpio20/direction

echo 1 > /sys/class/gpio/gpio20/value

