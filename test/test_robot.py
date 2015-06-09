"""Unit tests for Robot submodule."""

import unittest
import tempfile, os, time
from motor_controller import MotorController
from robot import Robot
from robot import VelocityPidOutput
from robot import YawPidOutput
from pid import Pid
from mpu import Mpu
from qep import Qep
from pwm import Pwm

class RobotTest(unittest.TestCase):
        
    def setUp(self):
        # set up a temporary directory tree to satisfy the Pwm members of robot
        tmpdir = tempfile.mkdtemp()
        # Create a temporary node tree
        self.PWM_A = tmpdir + Pwm.PORTS[Robot.MOTOR_A_PWM]
        self.PWM_A_DIR = self.PWM_A + ".0"
        Pwm.PORTS[Robot.MOTOR_A_PWM] = self.PWM_A
        self.PWM_B = tmpdir + Pwm.PORTS[Robot.MOTOR_B_PWM]
        self.PWM_B_DIR = self.PWM_B + ".1"
        Pwm.PORTS[Robot.MOTOR_B_PWM] = self.PWM_B
        self.PWM_C = tmpdir + Pwm.PORTS[Robot.MOTOR_C_PWM]
        self.PWM_C_DIR = self.PWM_C + ".2"
        Pwm.PORTS[Robot.MOTOR_C_PWM] = self.PWM_C
        if not os.path.exists(self.PWM_A_DIR):
            os.makedirs(self.PWM_A_DIR)
        if not os.path.exists(self.PWM_B_DIR):
            os.makedirs(self.PWM_B_DIR)
        if not os.path.exists(self.PWM_C_DIR):
            os.makedirs(self.PWM_C_DIR)
        # set up a temporary directory tree to satisfy the Pwm and Qep members of robot
        # Create a temporary node tree
        self.QEP_A = tmpdir + Qep.PORTS[Robot.MOTOR_A_QEP]
        self.QEP_A_DIR = self.QEP_A
        Qep.PORTS[Robot.MOTOR_A_QEP] = self.QEP_A
        self.QEP_B = tmpdir + Qep.PORTS[Robot.MOTOR_B_QEP]
        self.QEP_B_DIR = self.QEP_B
        Qep.PORTS[Robot.MOTOR_B_QEP] = self.QEP_B
        self.QEP_C = tmpdir + Qep.PORTS[Robot.MOTOR_C_QEP]
        self.QEP_C_DIR = self.QEP_C
        Qep.PORTS[Robot.MOTOR_C_QEP] = self.QEP_C
        if not os.path.exists(self.QEP_A_DIR):
            os.makedirs(self.QEP_A_DIR)
        if not os.path.exists(self.QEP_B_DIR):
            os.makedirs(self.QEP_B_DIR)
        if not os.path.exists(self.QEP_C_DIR):
            os.makedirs(self.QEP_C_DIR)
    
    def test_robot_init(self):
        r = Robot()
        self.assertEqual(r.yaw_pid_enabled, True)
        self.assertTrue(isinstance(r.yaw_pid, Pid))
        self.assertTrue(isinstance(r.mpu, Mpu))
        self.assertTrue(isinstance(r.motor_a, MotorController))
        self.assertTrue(isinstance(r.motor_b, MotorController))
        self.assertTrue(isinstance(r.motor_c, MotorController))
        self.assertEqual(r.current_command, Robot.INIT_COMMAND)
        
        time.sleep(1)
        
        print "after boing"
        
    def test_robot_drive(self):
        
        r = Robot()
        r.yaw_pid_enabled = False # turn off PID so we dont have it messing with the tests
        
        r.drive(0.0, 0.0, 0.0, 0.0)
        
        self.assertEqual(r.motors[0].pid.get_set_point(), 0.0)
        
        r.drive(0.0, 1.0, 0.0, 1.0)
        
        self.assertAlmostEqual(r.motors[0].pid.get_set_point(), 0.5)