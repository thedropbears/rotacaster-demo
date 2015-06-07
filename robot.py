"""Main robot class"""

import math
from pid import Pid, PidOutput
from pwm import Pwm
from qep import Qep
from mpu import Mpu
from motor_controller import MotorController

class Robot(object):
    
    VEL_P = 0
    VEL_I = 0
    VEL_D = 0
    VEL_F = 1.0
    
    YAW_P = 0
    YAW_I = 0
    YAW_D = 0
    
    # Pwm and Qep ids for motor controllers a, b and c
    MOTOR_A_PWM = "PWM1A-14"
    MOTOR_A_QEP = "QEP0"
    MOTOR_B_PWM = "PWM1A-36"
    MOTOR_B_QEP = "QEP1"
    MOTOR_C_PWM = "PWM1B-16"
    MOTOR_C_QEP = "QEP2"
    
    INIT_COMMAND = "OmniDrive" # placeholder
    
    VEL_PID_ENABLED = True
    
    ROBOT_MAX_X_SPEED = math.sin(math.radians(60)) # approx 0.87 (root 2 over 3)
    ROBOT_MAX_Y_SPEED = math.cos(math.radians(60)) #  0.50
    
    def __init__(self):
        # Velocity PID object setup
        self.vel_pid_output_a = VelocityPidOutput()
        self.vel_pid_output_b = VelocityPidOutput()
        self.vel_pid_output_c = VelocityPidOutput()
        self.vel_pid_a = Pid(self.vel_pid_output_a, Robot.VEL_P, Robot.VEL_I, Robot.VEL_D, Robot.VEL_F)
        self.vel_pid_b = Pid(self.vel_pid_output_b, Robot.VEL_P, Robot.VEL_I, Robot.VEL_D, Robot.VEL_F)
        self.vel_pid_c = Pid(self.vel_pid_output_c, Robot.VEL_P, Robot.VEL_I, Robot.VEL_D, Robot.VEL_F)
        # Qep encoder object setup
        self.qep_a = Qep(Robot.MOTOR_A_QEP)
        self.qep_b = Qep(Robot.MOTOR_B_QEP)
        self.qep_c = Qep(Robot.MOTOR_C_QEP)
        # Pwm object setup
        self.pwm_a = Pwm(Robot.MOTOR_A_PWM)
        self.pwm_b = Pwm(Robot.MOTOR_B_PWM)
        self.pwm_c = Pwm(Robot.MOTOR_C_PWM)
        # Create MotorController objects
        self.motor_a = MotorController(self.pwm_a, self.vel_pid_a, self.vel_pid_output_a, self.qep_a, self.VEL_PID_ENABLED)
        self.motor_b = MotorController(self.pwm_b, self.vel_pid_b, self.vel_pid_output_b, self.qep_b, self.VEL_PID_ENABLED)
        self.motor_c = MotorController(self.pwm_c, self.vel_pid_c, self.vel_pid_output_c, self.qep_c, self.VEL_PID_ENABLED)
        self.motors = [self.motor_a, self.motor_b, self.motor_c]
        
        self.yaw_pid_output = YawPidOutput()
        self.yaw_pid = Pid(self.yaw_pid_output, Robot.YAW_P, Robot.YAW_I, Robot.YAW_D)
        self.mpu = Mpu()
        self.current_command = Robot.INIT_COMMAND
        
        self.yaw_pid_enabled = True
    
    def drive(self, vX, vY, vZ, throttle):
        
        # Drive equations that translate vX, vY and vZ into commands to be sent to the motors
        # front motor
        mA = ((0.0*vX) + (vY * Robot.ROBOT_MAX_Y_SPEED) + vZ)
        # bottom left motor
        mB = ((-vX * Robot.ROBOT_MAX_Y_SPEED /  Robot.ROBOT_MAX_X_SPEED) + (-vY * 1.0) + vZ)
        # bottom right motor
        mC = ((vX * Robot.ROBOT_MAX_Y_SPEED /  Robot.ROBOT_MAX_X_SPEED) + (-vY * 1.0) + vZ)
        
        motor_input = [mA, mB, mC]
        
        max = 1.0
        for i in range(3):
            if math.fabs(motor_input[i]) > max:
                max = abs(motor_input[i])
        
        for i in range(3):
            motor_input[i] = motor_input[i]/max
        
        for i in range(3):
            motor_input[i] *= throttle
        
        for i in range(3):
            self.motors[i].set_speed(motor_input[i])

class VelocityPidOutput(PidOutput):
    value = 0.0
    def set(self, value):
        self.value = value
        
class YawPidOutput(PidOutput):
    value = 0.0
    def set(self, value):
        self.value = value