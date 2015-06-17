import threading, time
from robot import Robot
from abc import ABCMeta, abstractmethod

class Commands(threading.Thread):
    """A class that holds all of the commands and runs the current one in a thread"""
    
    COMMAND_LOOP_SPEED = 50.0 #hz
    
    commands = {}
    
    DEFAULT_COMMAND = "OmniDrive"
    
    def __init__(self, robot, input):
        super(Commands, self).__init__()
        self.robot = robot
        self.input = input
        self.omni_drive = OmniDrive(self)
        self.commands["OmniDrive"]= self.omni_drive
        self.current_command = self.commands[self.DEFAULT_COMMAND]
        self.last_command = self.current_command
        self.running = threading.Event()
        self.running.set()
        self.daemon = True
        self.last_time = time.time()
        self.start()
        
    def handle_commands(self):
        if not self.current_command == self.last_command:
            self.last_command.end()
            self.current_command.initialise()
            self.current_command.run()
        elif self.current_command.is_finished():
            self.current_command = self.commands[self.DEFAULT_COMMAND]
            self.last_command.end()
            self.current_command.initialise()
            self.current_command.run()
            self.last_command = self.current_command
        else:
            self.current_command.run()
    
    def set_command(self, command_id):
        if command_id in self.commands.keys():
            self.current_command = self.commands[command_id]
        else:
            print "Can not pass in invalid command"
    
    def run(self):
        while self.running.isSet():
            self.handle_commands()
            time.sleep(1.0/self.COMMAND_LOOP_SPEED - (time.time() - self.last_time))
            self.last_time = time.time()

class Command(object):
    """Base class for all commands"""
    __metaclass__ = ABCMeta
    
    def __init__(self, name, commands):
        self.name = name
        self.commands = commands
    
    @abstractmethod
    def initialise(self):
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

class OmniDrive(Command):
    
    def __init__(self, commands):
        super(OmniDrive, self).__init__("OmniDrive", commands)
    
    def initialise(self):
        pass
    
    def run(self):
        # placeholder code until gamepad drivers are written
        vX = self.commands.input.get_left_stick_y() # up and down on the joystick!
        vY = self.commands.input.get_left_stick_x()
        vZ = self.commands.input.get_right_stick_x()
        throttle = 1.0
        
        self.commands.robot.drive(vX, vY, vZ, throttle)
    
    def is_finished(self):
        return True
    
    def end(self):
        self.commands.robot.drive(0.0, 0.0, 0.0, 0.0)