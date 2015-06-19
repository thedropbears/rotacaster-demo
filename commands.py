import threading, time
from robot import Robot
from abc import ABCMeta, abstractmethod
import math

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
        self.circle_drive = CircleDrive(self)
        self.commands["OmniDrive"]= self.omni_drive
        self.commands["SquareDrive"]=self.square_drive
        self.commands["CircleDrive"]=self.circle_drive
        self.current_command = self.commands[self.DEFAULT_COMMAND]
        self.last_command = self.current_command
        self.running = threading.Event()
        self.running.set()
        self.daemon = True
        self.last_time = time.time()
        self.start()
        
    def handle_commands(self):
        if not self.commands[self.robot.current_command] == self.last_command or self.robot.interrupted:
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
        self.robot.interrupted = False
        
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
        pass #self.commands.robot.drive(0.0, 0.0, 0.0, 0.0)

class SquareDrive(Command):
    
    #      vX, vY
    FORWARD = [1.0, 0,0]
    RIGHT = [0.0, -1.0]
    BACK = [-1.0, 0.0]
    LEFT = [0.0, 1.0]
    order = [RIGHT, BACK, LEFT, FORWARD]
    
    SEGMENT_DURATION = 4
    CARTESIAN_SCALE = 0.5
    
    def __init__(self, commands):
        super(SquareDrive, self).__init__("SquareDrive", commands)
        self.current_direction = 0
        self.last_segment_time = time.time()
        self.initialising = True
    
    def initialise(self):
        self.commands.robot.mpu.zero_yaw()
        self.initialising = True
        self.last_segment_time = time.time()
        self.current_direction = 0
    
    def run(self):
        if self.initialising:
            # Drive to a corner to begin
            if time.time() - self.last_segment_time > self.SEGMENT_DURATION/2.0:
                self.initialising = False
                self.last_segment_time = time.time()
            else:
                self.commands.robot.drive(1.0, 1.0, 0.0, self.CARTESIAN_SCALE)
            return
        if time.time() - self.last_segment_time  > self.SEGMENT_DURATION:
            self.current_direction = (self.current_direction + 1) % len(self.order)
            self.last_segment_time = time.time()
        
        self.commands.robot.drive(self.order[self.current_direction][0]*self.CARTESIAN_SCALE,
                                  self.order[self.current_direction][1]*self.CARTESIAN_SCALE,
                                  1.0, 1.0)
    
    def is_finished(self):
        return False # Run until stopped
    
    def end(self):
        self.commands.robot.drive(0.0, 0.0, 0.0, 0.0)

class CircleDrive(Command):
        
    CIRCLE_DURATION = 20
    CARTESIAN_SCALE = 0.6

    def __init__(self, commands):
        super(CircleDrive, self).__init__("CircleDrive", commands)
        self.start_time = time.time()
        self.initialising = True
    
    def initialise(self):
        self.commands.robot.mpu.zero_yaw()
        self.initialising = True
        self.start_time = time.time()
        self.current_direction = 0
    
    def run(self):
        if self.initialising:
            # Drive to a corner to begin
            if time.time() - self.start_time > self.CIRCLE_DURATION/(2.0*3.14):
                self.initialising = False
                self.start_time = time.time()
            else:
                self.commands.robot.drive(1.0, 0.0, 0.0, self.CARTESIAN_SCALE)
            return
        
        omega = (time.time() - self.start_time)/self.CIRCLE_DURATION * 2.0 * 3.14159
        self.commands.robot.drive(-math.sin(omega)*self.CARTESIAN_SCALE,
                                  math.cos(omega)*self.CARTESIAN_SCALE, 1.0, 1.0)
    
    def is_finished(self):
        return False # Run until stopped
    
    def end(self):
        self.commands.robot.drive(0.0, 0.0, 0.0, 0.0)

