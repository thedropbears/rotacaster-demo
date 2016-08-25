#!/usr/bin/env python

"""Main file to run the Rotacaster demo bot."""

from pwm import Pwm
import pygame
from pygame.locals import *
from commands import *
from BNO055 import bno055
import os, time
import logging, logging.handlers

MOTOR_A_PWM = "PWM0B-29"
MOTOR_B_PWM = "PWM1A-36"
MOTOR_C_PWM = "PWM2A-45"

STICK_DEADZONE = 0.05
DISABLE_TIME = 10

axis_map = {"left_stick_x" : 0, "left_stick_y" : 1, "right_stick_x" : 2, "right_stick_y" : 3}

button_map = {"a" : 1, "b" : 2, "x" : 0, "y" : 3,
              "left_button" : 4, "right_button" : 5,
              "left_trigger" : 6, "right_trigger" : 7,
              "back" : 8, "start" : 9,
              "left_stick_press" : 10, "right_stick_press" : 11}

loop_speed = 1/50.0 #loop speed, seconds

def main():
    pid = str(os.getpid())
    file("/var/run/rotacaster.pid", "w").write(pid)
    # Setup network logging
    rootlogger = logging.getLogger('')
    rootlogger.setLevel(logging.DEBUG)
    socket_handler = logging.handlers.SocketHandler('localhost',
        logging.handlers.DEFAULT_TCP_LOGGING_PORT)
    rootlogger.addHandler(socket_handler)
    logger = logging.getLogger('rotacaster')

    pwm_a = Pwm(MOTOR_A_PWM)
    pwm_b = Pwm(MOTOR_B_PWM)
    pwm_c = Pwm(MOTOR_C_PWM)
    pwms = [pwm_a, pwm_b, pwm_c]
    for p in pwms:
        p.pwm_off()
    gyro = bno055(addr=0x28, busnum=2)

    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.init()
    js = pygame.joystick.Joystick(0)
    js.init()
    axis = [0.0 for x in range(len(axis_map))]
    last_input = time.time()
    rotation_locker = 0.0

    command = None
    last_loop = time.time()

    while True:
        #wait until we want to start next loop
        while time.time()-last_loop<loop_speed:
            pass

        last_loop = time.time()

        active_buttons = [False for x in range(max(button_map.values())+1)] # Zero indexed, so add one
        for event in pygame.event.get():
            if event.type == JOYAXISMOTION:
                if event.axis < len(axis_map):
                    axis[event.axis] = event.value
            elif event.type == JOYBUTTONDOWN and event.button < len(button_map):
                logger.info("Button pressed: %i" % (event.button))
                active_buttons[event.button] = True

        if True in [abs(val)>STICK_DEADZONE for val in axis] or True in active_buttons:
            last_input = time.time()

        # first check for enabling
        if (active_buttons[button_map["left_button"]]
            and active_buttons[button_map["right_button"]]):
            logger.info("Enabled")
            command = drive
            for p in pwms:
                p.pwm_on()

        # disable if we haven't moved the sticks in a while
        disable_buttons = (active_buttons[button_map["left_trigger"]] or
            active_buttons[button_map["right_trigger"]])
        timeout = (time.time() - last_input > DISABLE_TIME
                and command is drive
                and not rotation_locker)

        if disable_buttons or timeout:
            logger.info("Disabled")
            command = None
            for p in pwms:
                p.pwm_off()
            rotation_locker = 0.0
        
        # reset gyro
        if active_buttons[button_map["start"]]:
            logger.info("Reset gyro")
            gyro.reset_heading()

        if not command:
            continue
        
        # if we are moving the sticks
        if True in [abs(val)>STICK_DEADZONE for val in axis]:
            command = drive

        # lock/unlock rotation
        if active_buttons[button_map["right_stick_press"]]:
            if rotation_locker:
                logger.info("Unlock rotation")
                rotation_locker = 0.0
            elif abs(axis[axis_map["right_stick_x"]]) > STICK_DEADZONE * 2.0:
                logger.info("Lock rotation")
                rotation_locker = axis[axis_map["right_stick_x"]]

        # run canned movement routines
        if active_buttons[button_map["a"]] and command is drive:
            logger.info("Running square routine")
            #command = square
        if active_buttons[button_map["b"]] and command is drive:
            logger.info("Running circle routine")
            #command = circle
        
        # Run the particular command that is set
        if command is drive:
            command = command(
                        axis[axis_map["left_stick_y"]],
                        axis[axis_map["left_stick_x"]],
                        rotation_locker if rotation_locker else axis[axis_map["right_stick_x"]],
                        1.0, gyro, pwms
                    )
        else:
            command = command(gyro, pwms)

        #logger.debug(gyro.get_heading())




if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import sys, traceback
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        pa = Pwm(MOTOR_A_PWM)
        pb = Pwm(MOTOR_B_PWM)
        pc = Pwm(MOTOR_C_PWM)
        pa.set_speed(0.0)
        pb.set_speed(0.0)
        pc.set_speed(0.0)
        print "Exception Thrown, all motors stopped"
