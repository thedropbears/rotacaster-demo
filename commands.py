import threading, time
from robot import Robot
from abc import ABCMeta, abstractmethod

class Commands(threading.Thread):
    """A class that holds all of the commands and runs the current one in a thread"""
    
    COMMAND_LOOP_SPEED = 10.0 #hz
    
    commands = {}
    
    DEFAULT_COMMAND = "OmniDrive"
    
    def __init__(self, robot, input):
        super(Commands, self).__init__()
        self.robot = robot
        self.input = input
        self.omni_drive = OmniDrive(self)
        self.square_drive = SquareDrive(self)
        self.commands["OmniDrive"]= self.omni_drive
        self.commands["SquareDrive"]=self.square_drive
        self.current_command = self.commands[self.DEFAULT_COMMAND]
        self.last_command = self.current_command
        self.running = threading.Event()
        self.running.set()
        self.daemon = True
        self.last_time = time.time()
        self.start()
        
    def handle_commands(self):
        if not self.commands[self.robot.current_command] == self.last_command:
            self.last_command.end()
            self.last_command = self.commands[self.robot.current_command]
            self.commands[self.robot.current_command].initialise()
            self.commands[self.robot.current_command].run()
        elif self.commands[self.robot.current_command].is_finished():
            self.robot.current_command = Robot.INIT_COMMAND
            self.last_command.end()
            self.commands[self.robot.current_command].initialise()
            self.commands[self.robot.current_command].run()
            self.last_command = self.commands[self.robot.current_command]
        else:
            self.commands[self.robot.current_command].run()
    
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
        vX = self.commands.input.get_left_stick_y() # up and down on the joystick!
        vY = self.commands.input.get_left_stick_x()
        vZ = self.commands.input.get_right_stick_x()
        throttle = 1.0
        
        self.commands.robot.drive(vX, vY, vZ, throttle)
    
    def is_finished(self):
        return True
    
    def end(self):
        self.commands.robot.drive(0.0, 0.0, 0.0, 0.0)

class SquareDrive(Command):
    
    #      vX, vY
    FORWARD = [1.0, 0,0]
    RIGHT = [0.0, -1.0]
    BACK = [-1.0, 0.0]
    LEFT = [0.0, 1.0]
    order = [FORWARD, RIGHT, BACK, LEFT]
    
    QEP_THRESHOLD = 100
    
    def __init__(self, commands):
        super(SquareDrive, self).__init__("OmniDrive", commands)
        self.current_direction = 0
        print "__init__"
    
    def initialise(self):
        self.commands.robot.qep_a.set_position(0)
        self.commands.robot.qep_b.set_position(0)
        self.commands.robot.qep_c.set_position(0)
        print "init"
    
    def run(self):
        qep_average = (self.commands.robot.qep_a.get_revolutions() + self.commands.robot.qep_b.get_revolutions() + self.commands.robot.qep_c.get_revolutions())/3.0
        print "QEP AVG: ", qep_average
        if qep_average  > self.QEP_THRESHOLD:
            self.commands.robot.qep_a.set_position(0.0)
            self.commands.robot.qep_b.set_position(0.0)
            self.commands.robot.qep_c.set_position(0.0)
            if not self.current_direction >= len(self.order) - 1:
                self.current_direction += 1
            else:
                self.commands.robot.drive(0.0, 0.0, 0.0, 0,0)
                return
        print "running in square"
        
        self.commands.robot.drive(self.order[self.current_direction][0], self.order[self.current_direction][1], 1.0, 1.0)
    
    def is_finished(self):
        if not self.current_direction >= len(self.order) - 1:
            return False
        else:
            return True
    
    def end(self):
        self.commands.robot.drive(0.0, 0.0, 0.0, 0.0)