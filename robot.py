"""Main robot class"""

import math
from pid import Pid, PidOutput
from pwm import Pwm
from qep import Qep
from mpu import Mpu
from motor_controller import MotorController
import threading, time

class Robot(object):
    
    VEL_P = 0.0
    VEL_I = 0.0
    VEL_D = 0.0
    VEL_F = 1.0
    
    YAW_P = 0.0
    YAW_I = 0
    YAW_D = 0
    
    # Pwm and Qep ids for motor controllers a, b and c
    MOTOR_A_PWM = "PWM0B-29"
    MOTOR_A_QEP = "QEP0"
    MOTOR_B_PWM = "PWM1A-36"
    MOTOR_B_QEP = "QEP1"
    MOTOR_C_PWM = "PWM2A-45"
    MOTOR_C_QEP = "QEP2"
    
    INIT_COMMAND = "OmniDrive"
    
    VEL_PID_ENABLED = True
    
    ROBOT_MAX_X_SPEED = math.sin(math.radians(60)) # approx 0.87 (root 2 over 3)
    ROBOT_MAX_Y_SPEED = math.cos(math.radians(60)) #  0.50
    
    # the speed of rotation at which we shut down the pid so it does not oscillate
    # as you set the set point while still rotating
    YAW_MOMENTUM_THRESHOLD = math.radians(10.0) # degrees per second
    
    TIME_TO_AUTO_DISABLE = 10 # seconds till we automatically disable
    AUTO_DISABLE_THRESHOLD = 0.05
    
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
        self.pwms = [self.pwm_a, self.pwm_b, self.pwm_c]
        
        # Create MotorController objects
        self.motor_a = MotorController(self.pwm_a, self.vel_pid_a, self.vel_pid_output_a, self.qep_a, self.VEL_PID_ENABLED)
        self.motor_b = MotorController(self.pwm_b, self.vel_pid_b, self.vel_pid_output_b, self.qep_b, self.VEL_PID_ENABLED)
        self.motor_c = MotorController(self.pwm_c, self.vel_pid_c, self.vel_pid_output_c, self.qep_c, self.VEL_PID_ENABLED)
        self.motors = [self.motor_a, self.motor_b, self.motor_c]
        
        # set up pid
        self.yaw_pid_output = YawPidOutput()
        self.yaw_pid = Pid(self.yaw_pid_output, Robot.YAW_P, Robot.YAW_I, Robot.YAW_D, izone=1.0)
        
        # initialise mpu/imu server module
        self.mpu = Mpu()
        
        self.yaw_pid_thread = YawPidThread(self.yaw_pid, self.mpu)
        
        self.current_command = Robot.INIT_COMMAND
        
        # pid *enabled* by default
        self.yaw_pid_enabled = False
        # pid not in *control* by default, this is automatically set by drive
        self.pid_in_control = False
        
        self.field_centered = True
        
        self.enabled = False
        
        self.last_input_time = time.time()
    
    def drive(self, vX, vY, vZ, throttle):
        
        if not self.enabled:
            self.last_input_time = time.time()
            for motor in self.motors:
                motor.set_speed(0.0)
            for p in self.pwms:
                p.set_speed(0.0)
                p.pwm_off()
            return
        if math.fabs(vX) <= self.AUTO_DISABLE_THRESHOLD and math.fabs(vY) <= self.AUTO_DISABLE_THRESHOLD and math.fabs(vZ) <= self.AUTO_DISABLE_THRESHOLD:
            if time.time() - self.last_input_time > self.TIME_TO_AUTO_DISABLE:
                self.enabled = False
        else:
            for p in self.pwms:
                p.pwm_on()
            self.last_input_time = time.time()
        
        vPID = 0.0
        
        if self.field_centered:
            vX, vY = self.field_orient(vX, vY, self.mpu.get_euler()[0])
        
        # Drive equations that translate vX, vY and vZ into commands to be sent to the motors
        # front motor
        mA = (((0.0*vX) + (vY * 1.0))/2.0 + vZ/3.0)
        # bottom left motor
        mB = (((-vX * math.sin(math.radians(60))) + (-vY / 2.0))/2.0 + vZ/3.0)
        # bottom right motor
        mC = (((vX * math.sin(math.radians(60))) + (-vY / 2.0))/2.0 + vZ/3.0)
        
        motor_input = [mA, mB, mC]
        
        if self.yaw_pid_enabled:
            if not vZ == 0:
                # spinning under command -> no PID
                self.pid_in_control = False
            elif math.fabs(self.mpu.get_gyro()[2]) < Robot.YAW_MOMENTUM_THRESHOLD:
                # momentum is less than the threshold and we are not under command
                # -> PID can now take control
                self.pid_in_control = True
            
            if self.pid_in_control:
                vPID = self.yaw_pid_output.value
            else:
                heading = self.mpu.get_euler()[0] # yaw
                self.yaw_pid.set_set_point(heading)
                # zero the correction value so that the next time the code runs the existing
                # correction value will not still be there
                self.yaw_pid_output.value = 0.0
        
        max = 1.0
        # find the maximum motor speed
        for i in range(3):
            if math.fabs(motor_input[i]) > max:
                max = abs(motor_input[i])
        
        # scale between -1 and 1
        for i in range(3):
            motor_input[i] /= max
        
        # multiply by throttle
        for i in range(3):
            motor_input[i] *= throttle
        
        if self.yaw_pid_enabled:
            max = 1
            
            for i in range(3):
                motor_input[i] -= vPID
                if math.fabs(motor_input[i]) > max:
                    max = math.fabs(motor_input[i])
            
            for i in range(3):
                motor_input[i] /= max
        
        # set the speeds of the motors
        for i in range(3):
            self.motors[i].set_speed(motor_input[i])
    
    def field_orient(self, vX, vY, yaw_angle):
        oriented_vx = vX*math.cos(yaw_angle)+vY*math.sin(yaw_angle)
        oriented_vy = -vX*math.sin(yaw_angle)+vY*math.cos(yaw_angle)
        return oriented_vx, oriented_vy

class YawPidThread(threading.Thread):
    def __init__(self, pid, mpu):
        if not isinstance(pid, Pid):
            raise Exception("Must pass in valid Pid object to YawPidThread")
        if not isinstance(mpu, Mpu):
            raise Exception("Must pass in valid Mpu object to YawPidThread")
        super(YawPidThread, self).__init__()
        self.pid = pid
        self.mpu = mpu
        self.running = threading.Event()
        self.running.set()
        self.daemon = True
        self.last_time = time.time()
        self.start()
    
    def run(self):
        while self.running.isSet():
            self.pid.update(self.mpu.get_euler()[0])
            time.sleep(0.1 - (time.time() - self.last_time))
            self.last_time = time.time()

class VelocityPidOutput(PidOutput):
    value = 0.0
    def set(self, value):
        self.value = value
        
class YawPidOutput(PidOutput):
    value = 0.0
    def set(self, value):
        self.value = value
