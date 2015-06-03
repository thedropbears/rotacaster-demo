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
        """Create a temporary node tree to satisfy the Pwm and Qep classes in motorcontroller"""
        tmpdir = tempfile.mkdtemp()
        # Create a temporary node tree
        self.PWM99A = tmpdir + "/sys/devices/ocp.3/pwm_test_P9_99"
        self.PWM99A_dir = self.PWM99A + '.12' # Device tree files have an incrementing .XX suffix
        Pwm.PORTS["PWM99A"] = self.PWM99A
        if not os.path.exists(self.PWM99A_dir):
            os.makedirs(self.PWM99A_dir)
        self.QEP99 = tmpdir + "/sys/devices/ocp.2/48306000.epwmss/48306180.eqep"
        self.QEP99_dir = self.QEP99
        Qep.PORTS["QEP99"] = self.QEP99
        if not os.path.exists(self.QEP99_dir):
            os.makedirs(self.QEP99_dir)
    
    def test_motor_controller_init(self):
        p = Pwm("PWM99A", MotorController.MOTOR_CONTROLLER_VALUES["VICTOR_SP"]["min_duty"],
                MotorController.MOTOR_CONTROLLER_VALUES["VICTOR_SP"]["max_duty"],
                MotorController.MOTOR_CONTROLLER_VALUES["VICTOR_SP"]["period"])
        
        pid_output = VelocityPidOutput()
        p_controller = Pid(pid_output, 1.0, 0.0, 0.0, 1.0, set_point = 0.0)
        
        q = Qep("QEP99", Qep.MODE_RELATIVE, 360, 10000000, 0.0)
        
        m = MotorController(p, p_controller, q)
        
        self.assertTrue(isinstance(m, Thread))
        self.assertTrue(isinstance(m.pwm, Pwm))
        self.assertTrue(isinstance(m.qep, Qep))
        self.assertTrue(isinstance(m.pid, Pid))
        self.assertTrue(isinstance(m.pid_output, VelocityPidOutput))
        
        # Test default values
        self.assertEqual(m.pid_enabled, True)
        
        # Test non defualt values