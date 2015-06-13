import threading
from robot import Robot
from abc import ABCMeta, abstractmethod

class Commands(threading.Thread):
    """A class that holds all of the commands and runs the current one in a thread"""
    
    COMMAND_LOOP_SPEED = 50.0 #hz
    
    COMMANDS = {"OmniDrive" : OmniDrive()}
    
    def __init__(self, robot, init_command):
        super(YawPidThread, self).__init__()
        self.robot = robot
        self.current_command = current_command
        self.last_command = current_command
        if not isinstance(robot, Robot):
            raise Exception("Must pass in a valid Robot object for the robot parameter")
        if not init_command in self.COMMANDS.keys():
            raise Exception("Must pass in a valid command string. Check Commands.COMMANDS")
        self.running = threading.Event()
        self.running.set()
        self.daemon = True
        self.last_time = time.time()
        self.start()
        
    def commands(self):
        pass
    
    def run(self):
        while self.running.isSet():
            self.commands()
            time.sleep(1.0/self.COMMAND_LOOP_SPEED - (time.time() - self.last_time))
            self.last_time = time.time()

class Command(object):
    """Base class for all commands"""
    __metaclass__ = ABCMeta
    
    def __init__(self, name, commands):
        self.name = name
        self.commands = commands
        assert(isinstance(robot, Robot), "Must pass in a valid robot object to the command constructor")
    
    @abstractmethod
    def initialize(self):
        """Called by commands when this command is started"""
        pass
    
    @abstractmethod
    def run(self):
        """What is called once every 50 Hz"""
        pass
    
    @abstractmethod
    def is_finished(self):
        """Must return True or False based on weather that command has finished executing"""
        pass
    
    @abstractmethod
    def end(self):
        """Called by commands when this command is ended"""
        pass

class OmniDrive(object):
    
    def __init__(self, commands):
        super.__init__("OmniDrive", commands)
    
    def initialize(self, robot):
        pass
    
    def run(self):
        # placeholder code until gamepad drivers are written
        vX = 0.0 # up and down on the joystick!
        vY = 0.0
        vZ = 0.0
        throttle = 0.0
        
        self.commands.robot.drive(vX, vY, vZ, throttle)
    
    def is_finished(self):
        return True
    
    def end(self):
        robot.drive(0.0, 0.0, 0.0, 0.0)