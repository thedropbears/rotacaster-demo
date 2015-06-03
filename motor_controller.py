"""A class that combines Pwm outputs with Qep based Pid for velocity control"""

from pwm import Pwm
from qep import Qep
from pid import Pid, PidOutput
from pid import PidOutput
from threading import Thread

class MotorController(Thread):
    
    #list of motor controllers with pwm values in a dict inside the dict
    MOTOR_CONTROLLER_VALUES = {"VICTOR_SP" : {"min_duty" : 600000, "max_duty" : 2400000, "period" : 10000000}}
    
    def __init__(self, pwm, pid, qep, pid_enabled = True):
        self.pwm = pwm
        self.pid = pid
        self.qep = qep
        self.pid_output = self.pid.getOutput()
        self.pid_enabled = pid_enabled
        self.qep_period = 10000000 # 1/100th of a second (in ns)
        if self.pid_enabled and self.pid.kF == 0:
            raise Exception("Cannot enable PID while kF is set to a zero value for velocity control")

class VelocityPidOutput(PidOutput):
    correction = 0
    def set(self, value):
        self.correction = value