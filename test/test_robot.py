"""Unit tests for Robot submodule."""

import unittest
import tempfile, os
from pwm import Pwm
from robot import Robot
from robot import VelocityPidOutput
from robot import YawPidOutput
from pid import Pid
from mpu import Mpu
from qep import Qep

class RobotTest(unittest.TestCase):
        
    def setUp(self):
        # set up a temporary directory tree to satisfy the Pwm members of robot
        tmpdir = tempfile.mkdtemp()
        # Create a temporary node tree
        self.MOTOR_A = tmpdir + Pwm.PORTS[Robot.MOTOR_A_ID]
        self.MOTOR_A_DIR = self.MOTOR_A + ".0"
        Pwm.PORTS[Robot.MOTOR_A_ID] = self.MOTOR_A
        self.MOTOR_B = tmpdir + Pwm.PORTS[Robot.MOTOR_B_ID]
        self.MOTOR_B_DIR = self.MOTOR_B + ".1"
        Pwm.PORTS[Robot.MOTOR_B_ID] = self.MOTOR_B
        self.MOTOR_C = tmpdir + Pwm.PORTS[Robot.MOTOR_C_ID]
        self.MOTOR_C_DIR = self.MOTOR_C + ".2"
        Pwm.PORTS[Robot.MOTOR_C_ID] = self.MOTOR_C
        if not os.path.exists(self.MOTOR_A_DIR):
            os.makedirs(self.MOTOR_A_DIR)
        if not os.path.exists(self.MOTOR_B_DIR):
            os.makedirs(self.MOTOR_B_DIR)
        if not os.path.exists(self.MOTOR_C_DIR):
            os.makedirs(self.MOTOR_C_DIR)
    
    def test_robot_init(self):
        r = Robot()
        self.assertEqual(r.yaw_pid_on, True)
        self.assertEqual(r.vel_pid_on, True)
        self.assertTrue(isinstance(r.yaw_pid, Pid))
        self.assertTrue(isinstance(r.vel_pid, Pid))
        self.assertTrue(isinstance(r.mpu, Mpu))
        self.assertTrue(isinstance(r.motor_a, Pwm))
        self.assertTrue(isinstance(r.motor_b, Pwm))
        self.assertTrue(isinstance(r.motor_c, Pwm))
        self.assertTrue(isinstance(r.vel_pid, Pid))
        self.assertTrue(isinstance(r.yaw_pid, Pid))
        self.assertTrue(isinstance(r.vel_pid_output, VelocityPidOutput))
        self.assertTrue(isinstance(r.yaw_pid_output, YawPidOutput))
        self.assertEqual(r.current_command, Robot.INIT_COMMAND)