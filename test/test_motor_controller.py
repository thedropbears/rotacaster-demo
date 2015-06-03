"""Unit tests for the motor controller submodule"""

import unittest
from motor_controller import MotorController, VelocityPidOutput
from qep import Qep
from robot import Robot
from pwm import Pwm
from pid import Pid
from threading import Thread
import tempfile, os

class MotorControllerTest(unittest.TestCase):
    
    def setUp(self):
        """Create a temporary node tree to satisfy the Pwm class in motorcontroller"""
        tmpdir = tempfile.mkdtemp()
        # Create a temporary node tree
        self.PWM99A = tmpdir + "/sys/devices/ocp.3/pwm_test_P9_99"
        self.PWM99A_dir = self.PWM99A + '.12' # Device tree files have an incrementing .XX suffix
        Pwm.PORTS["PWM99A"] = self.PWM99A
        if not os.path.exists(self.PWM99A_dir):
            os.makedirs(self.PWM99A_dir)
    
    def test_motor_controller_init(self):
        m = MotorController(MotorController.MOTOR_CONTROLLER_VALUES["VICTOR_SP"], Robot.MOTOR_A_ID, Qep.PORTS["QEP1"])
        
        self.assertTrue(isinstance(m, Thread))
        self.assertTrue(isinstance(m.pwm, Pwm))
        self.assertTrue(isinstance(m.qep, Qep))
        self.assertTrue(isinstance(m.pid, Pid))
        self.assertTrue(isinstance(m.pid_output, VelocityPidOutput))
        
        # Test default values
        self.assertEqual(m.pid_enabled, False)
        
        # Test non defualt falues
        m = MotorController(MotorController.MOTOR_CONTROLLER_VALUES["VICTOR_SP"], Robot.MOTOR_A_ID, Qep.PORTS["QEP1"], True, P = 1.0, I = 0.0, D = 0.0, F = 1.0)
        
        self.assertEqual(m.pid_enabled, True)
        self.assertEqual(m.P, 1.0)
        self.assertEqual(m.I, 0.0)
        self.assertEqual(m.D, 0.0)
        self.assertEqual(m.F, 1.0)