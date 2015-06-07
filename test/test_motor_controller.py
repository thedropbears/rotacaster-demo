"""Unit tests for the motor controller submodule"""

import unittest, time
from pid import PidOutput
from motor_controller import MotorController
from threading import Thread

class MockPwm(object):
    def set_speed(self, speed):
        self.speed = speed

class MockQep(object):
    def __init__(self):
        from qep import Qep
        self.mode = Qep.MODE_ABSOLUTE
    def get_revolutions(self):
        return 0

class MockPid(object):
    def __init__(self, pid_output):
        self.pid_output = pid_output
        self.kF = 1.0
        self.set_point = 0.0
    def update(self, value):
        self.pid_output.set(self.set_point)
    def set_set_point(self, set_point):
        self.set_point = set_point
        

class MockPidOutput(PidOutput):
    def set(self, value):
        self.value = value

class MotorControllerTest(unittest.TestCase):
    
    def setUp(self):
        p = MockPwm()
        
        self.p_output = MockPidOutput()
        p_controller = MockPid(self.p_output)
        
        q = MockQep()
        
        self.m = MotorController(p, p_controller, self.p_output, q)
        pass
    
    def test_motor_controller_init(self):
        
        self.assertTrue(isinstance(self.m, Thread))
        self.assertTrue(isinstance(self.m.pwm, MockPwm))
        self.assertTrue(isinstance(self.m.qep, MockQep))
        self.assertTrue(isinstance(self.m.pid, MockPid))

        # Test default values
        self.assertEqual(self.m.pid_enabled, True)
        
    def test_motor_controlling(self):
        
        self.m.set_speed(1.0)
        
        self.assertEqual(1.0, self.m.pid.set_point)
        
        time.sleep(0.2)
        
        self.assertEqual(self.p_output.value, 1.0)