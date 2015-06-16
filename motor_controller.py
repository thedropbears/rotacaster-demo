"""A class that combines Pwm outputs with Qep based Pid for velocity control"""

import threading, time
from pid import PidOutput
from qep import Qep

class MotorController(threading.Thread):
    
    #list of motor controllers with pwm values in a dict inside the dict
    MOTOR_CONTROLLER_VALUES = {"VICTOR_SP" : {"min_duty" : 600000, "max_duty" : 2400000, "period" : 10000000}}
    
    def __init__(self, pwm, pid, pid_output, qep, pid_enabled = True):
        super(MotorController, self).__init__()
        if qep.mode == Qep.MODE_RELATIVE:
            raise Exception("Must pas in a Qep object in absolute mode")
        self.pwm = pwm
        self.pid = pid
        self.qep = qep
        self.pid_output = pid_output
        self.pid_enabled = pid_enabled
        self.speed = 0
        if self.pid_enabled and self.pid.kF == 0:
            raise Exception("Cannot enable PID while kF is set to a zero value for velocity control")
        self.running = threading.Event()
        self.running.set()
        self.daemon = True
        self.last_time = time.time()
        self.last_qep = qep.get_revolutions()
        self.start()
    
    def run(self):
        while self.running.isSet():
            if self.pid_enabled:
                # Get the number of revolutions relative to the start point 
                self.qep_position = self.qep.get_revolutions()
                change_since_last = self.qep_position - self.last_qep # the change since the last iteration
                self.last_qep = self.qep_position
                self.pid.update(change_since_last)
                self.speed_to_command = self.pid_output.value
            else:
                self.speed_to_command = self.speed
            self.pwm.set_speed(self.speed_to_command)
            time.sleep(0.02 - (time.time() - self.last_time))
            self.last_time = time.time()
    
    def set_speed(self, speed):
        if speed >= 1.0:
            speed = 1.0
        elif speed <= -1.0:
            speed = -1.0
        if self.pid_enabled:
            self.pid.set_set_point(speed)
        self.speed = speed
    
class VelocityPidOutput(PidOutput):
    correction = 0
    def set(self, value):
        self.correction = value