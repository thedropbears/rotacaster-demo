"""Main robot class"""

from pid import Pid
from pid import PidOutput
from pwm import Pwm

class Robot(object):
    
    VEL_P = 0
    VEL_I = 0
    VEL_D = 0
    VEL_F = 0
    
    YAW_P = 0
    YAW_I = 0
    YAW_D = 0
    
    MOTOR_A_ID = "PWM1A-14"
    MOTOR_B_ID = "PWM1A-36"
    MOTOR_C_ID = "PWM1B-16"
    
    INIT_COMMAND = "OmniDrive" # placeholder
    
    def __init__(self):
        self.vel_pid_on = True
        self.vel_pid_output = VelocityPidOutput()
        self.vel_pid = Pid(self.vel_pid_output, Robot.VEL_P, Robot.VEL_I, Robot.VEL_D)
        self.yaw_pid_on = True
        self.yaw_pid_output = YawPidOutput()
        self.yaw_pid = Pid(self.yaw_pid_output, Robot.YAW_P, Robot.YAW_I, Robot.YAW_D)
        self.motor_a = Pwm(Robot.MOTOR_A_ID)
        self.motor_b = Pwm(Robot.MOTOR_B_ID)
        self.motor_c = Pwm(Robot.MOTOR_C_ID)
        self.current_command = Robot.INIT_COMMAND

class VelocityPidOutput(PidOutput):
    correction = 0
    def set(self, value):
        self.correction = value
        
class YawPidOutput(PidOutput):
    correction = 0
    def set(self, value):
        self.correction = value