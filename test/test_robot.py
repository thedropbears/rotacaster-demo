"""Unit tests for Robot submodule."""

import unittest
import tempfile, os
from robot import Robot
from robot import VelocityPidOutput
from robot import YawPidOutput
from pid import Pid
from mpu import Mpu
from pwm import Pwm
from qep import Qep

class RobotTest(unittest.TestCase):
    
    def setUp(self):
        # set up a temporary directory tree to satisfy the Pwm members of robot
        tmpdir = tempfile.mkdtemp()
        # Create a temporary node tree
        self.MOTOR_A_DIR = tmpdir + Pwm.PORTS[Robot.MOTOR_A_ID] + ".0"
        self.MOTOR_B_DIR = tmpdir + Pwm.PORTS[Robot.MOTOR_B_ID] + ".1"
        self.MOTOR_C_DIR = tmpdir + Pwm.PORTS[Robot.MOTOR_C_ID] + ".2"
        if not os.path.exists(self.MOTOR_A_DIR):
            os.makedirs(self.MOTOR_A_DIR)
        if not os.path.exists(self.MOTOR_B_DIR):
            os.makedirs(self.MOTOR_B_DIR)
        if not os.path.exists(self.MOTOR_C_DIR):
            os.makedirs(self.MOTOR_C_DIR)
    
    def test_robot_init(self):
        r = Robot()
        self.assertEqual(r.yaw_pid, True)
        self.assertEqual(r.vel_pid, True)
        self.assertTrue(isinstance(r.yaw_pid, Pid))
        self.assertTrue(isinstance(r.vel_pid, Pid))
        self.assertTrue(isinstance(r.mpu, Mpu))
        self.assertTrue(isinstance(r.motor_a, Pwm))
        self.assertTrue(isinstance(r.motor_b, Pwm))
        self.assertTrue(isinstance(r.motor_c, Pwm))
        self.assertTrue(isinstance(r.vel_pid, Pid))
        self.assertTrue(isinstance(r.yaw_pid, Pid))
        self.assertTrue(isinstance(r.vel_pid_output, VelcityPidOutput))
        self.assertTrue(isinstance(r.yaw_pid_output, YawPidOutput))
        self.assertEqual(r.current_command, Robot.INIT_COMMAND)