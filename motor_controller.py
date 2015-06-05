"""A class that combines Pwm outputs with Qep based Pid for velocity control"""

from pwm import Pwm
from qep import Qep
from pid import Pid, PidOutput
from pid import PidOutput
import threading
import time

class MotorController(threading.Thread):
    
    #list of motor controllers with pwm values in a dict inside the dict
    MOTOR_CONTROLLER_VALUES = {"VICTOR_SP" : {"min_duty" : 600000, "max_duty" : 2400000, "period" : 10000000}}
    
    def __init__(self, pwm, pid, qep, pid_enabled = True):
        super(MotorController, self).__init__()
        if qep.mode == Qep.MODE_RELATIVE:
            raise Exception("Must pas in a Qep object in absolute mode")
        self.pwm = pwm
        self.pid = pid
        self.qep = qep
        self.pid_enabled = pid_enabled
        self.speed = 0
        if self.pid_enabled and self.pid.kF == 0:
            raise Exception("Cannot enable PID while kF is set to a zero value for velocity control")
        self.running = threading.Event()
        self.running.set()
        self.daemon = True
        self.last_time = time.time()
        self.last_qep = qep.getRevolutions()
        self.start()
    
    def run(self):
        print "tick"
        while self.running.isSet():
            # Get the number of revolutions relative to the start point 
            print "tick"
            self.qep_position = self.qep.getRevolutions()
            change_since_last = self.qep_position - self.last_qep # the change since the last iteration
            self.last_qep = self.qep_position
            self.speed_after_pid = self.pid.update(change_since_last)
            self.pwm.set_speed(self.speed_after_pid)
            time.sleep(0.02 - (time.time() - self.last_time))
            self.last_time = time.time()
    
    def set_speed(self):
        pass
    
class VelocityPidOutput(PidOutput):
    correction = 0
    def set(self, value):
        self.correction = value