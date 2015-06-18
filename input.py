import pygame, threading, os, time
from pygame.locals import *

class Input(threading.Thread):
    """Class to take input from an F710 joystick"""
    
    MONITOR_JOYSTICK_SPEED = 10.0 # Hz
    
    axis_map = {"left_stick_x" : 0, "left_stick_y" : 1, "right_stick_x" : 2, "right_stick_y" : 3,
                     "left_trigger" : 4, "right_trigger" : 5}
    
    axis_values = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    
    button_map = {"a" : 0, "b" : 1, "x" : 2, "y" : 3, "left_button" : 4, "right_button" : 5, "back" : 6, "start" : 7, "left_stick_press" : 9, "right_stick_press" : 10}
    
    def __init__(self, robot):
        super(Input, self).__init__()
        self.robot = robot
        self.rotation_locker = False
        self.last_pressed = -1
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        pygame.init()
        self.js = pygame.joystick.Joystick(0)
        self.js.init()
        self.running = threading.Event()
        self.running.set()
        self.daemon = True
        self.last_time = time.time()
        self.start()
    
    def run(self):
        """Monitor the joystick at a cirtain speed"""
        while self.running.isSet():
            for event in pygame.event.get():
                if event.type == JOYAXISMOTION:
                    if event.axis <= 5:
                        if not event.axis == self.axis_map["right_stick_x"] or not self.rotation_locker:
                            self.axis_values[event.axis] = event.value
                            if event.axis == self.axis_map["left_trigger"] or event.axis == self.axis_map["right_trigger"]:
                                self.robot.enabled = False
                elif event.type == JOYBUTTONDOWN:
                    if event.button == self.button_map["start"]:
                        self.robot.mpu.zero_yaw()
                    elif event.button == self.button_map["right_stick_press"]:
                        self.rotation_locker = not self.rotation_locker
                        if not self.rotation_locker:
                            self.axis_values[self.axis_map["right_stick_x"]] = 0.0
                    elif event.button == self.button_map["right_button"] and self.last_pressed == self.button_map["left_button"]:
                        self.robot.enabled = True
                    elif event.button == self.button_map["a"]:
                        self.robot.current_command = "SquareDrive"
                    self.last_pressed = event.button
                    
            self.last_time = time.time()
    
    def get_left_stick_x(self):
        return self.axis_values[self.axis_map["left_stick_x"]]
    
    def get_left_stick_y(self):
        return self.axis_values[self.axis_map["left_stick_y"]]
    
    def get_right_stick_x(self):
        return self.axis_values[self.axis_map["right_stick_x"]]
    
    def get_right_stick_y(self):
        return self.axis_values[self.axis_map["right_stick_y"]]
    
    def get_left_trigger(self):
        return self.axis_values[self.axis_map["left_trigger"]]
    
    def get_right_trigger(self):
        return self.axis_values[self.axis_map["right_trigger"]]