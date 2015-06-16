import pygame, threading, os, time
from pygame.locals import *

class Input(threading.Thread):
    """Class to take input from an F710 joystick"""
    
    MONITOR_JOYSTICK_SPEED = 10 # Hz
    
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
                    print event
            time.sleep(1.0/self.MONITOR_JOYSTICK_SPEED - (time.time() - self.last_time))
            self.last_time = time.time()
