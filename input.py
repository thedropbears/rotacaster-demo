import pygame, threading, os, time
from pygame.locals import *

class Input(threading.Thread):
    """Class to take input from an F710 joystick"""
    
    MONITOR_JOYSTICK_SPEED = 10 # Hz
    
    axis_map = {"left_stick_x" : 0, "left_stick_y" : 1, "right_stick_x" : 2, "right_stick_y" : 3,
                     "left_trigger" : 4, "right_trigger" : 5}
    
    axis_values = [0.0, 0.0, 0.0, 0.0, 0.0]
    
    button_map = {"a" : 0, "b" : 1, "x" : 2, "y" : 3, "left_button" : 4, "right_button" : 5, "back" : 6, "start" : 7, "left_stick_press" : 9, "right_stick_press" : 10}
    
    def __init__(self):
        super(Input, self).__init__()
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
                        print event
                        self.axis_values[event.axis] = event.value
                elif event.type == JOYBUTTONDOWN:
                    pass
            time.sleep(1.0/self.MONITOR_JOYSTICK_SPEED - (time.time() - self.last_time))
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