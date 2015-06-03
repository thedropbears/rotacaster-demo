"""A class that combines Pwm outputs with Qep based Pid for velocity control"""

from pwm import Pwm
from qep import Qep
from pid import Pid, PidOutput
from pid import PidOutput
from threading import Thread

class MotorController(Thread):
    
    #list of motor controllers with pwm values in a dict inside the dict
    MOTOR_CONTROLLER_VALUES = {"VICTOR_SP" : {"min_duty" : 600000, "max_duty" : 2400000, "period" : 10000000}}
    
    def __init__(self, controller_values, pwm_id, qep_id, pid_enabled = False, kP=0.0, kI=0.0, kD=0.0, kF=0.0, cpr=360, qep_period = 10000000):
        self.controller_values = controller_values
        self.pwm_id = pwm_id
        self.qep_id = qep_id
        self.pid_enabled = pid_enabled
        self.kP = kP
        self.kI = kI
        self.kD = kD
        self.kF = kF
        self.cpr = cpr
        self.qep_period = 10000000 # 1/100th of a second (in ns)
        pwm = Pwm(self.pwm_id, self.controller_values["min_duty"], self.controller_values["max_duty"], self.controller_values["period"])
        if self.pid_enabled and self.f == 0:
            raise Exception("Cannot enable PID while kF is set to a zero value for velocity control")
        # We load a pid object so that it exists if the user wants to enable pid down the track
        self.pid_output = VelocityPidOutput()
        self.pid = pid(self.pid_output, self.p, self.i, self.d, self.f, set_point=0.0)
        qep = Qep(self.qep_id, Qep.MODE_ABSOLUTE, self.cpr, self.QEP_PERIOD, self.qep_period, position = 0)

class VelocityPidOutput(PidOutput):
    correction = 0
    def set(self, value):
        self.correction = value