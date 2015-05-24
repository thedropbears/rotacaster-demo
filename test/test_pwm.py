"""Unit tests for PID submodule."""

import unittest
from pwm import Pwm
import tempfile, os

class PwmTest(unittest.TestCase):
    
    def setUp(self):
        tmpdir = tempfile.makedtemp()
        os.croot(tmpdir)
    
    def test_pwm_output(self):
                
        pwm = Pwm(pwm.PWM1A)
        
        speed = pwm.set_speed(0)
        self.assertEqual(speed, 0)
        self.assertEqual(speed, int(open(pwm.PWM1A).read()))
        speed = pwm.set_speed(0.5)
        self.assertEqual(speed, pwm.MAX_FREQUENCY/2)
        self.assertEqual(speed, int(open(pwm.PWM1A).read()))
        speed = pwm.set_speed(-0.5)
        self.assertEqual(speed, -pwm.MAX_FREQUENCY/2)
        self.assertEqual(speed, int(open(pwm.PWM1A).read()))
        speed = pwm.set_speed(1.0)
        self.assertEqual(speed, pwm.MAX_FREQUENCY)
        self.assertEqual(speed, int(open(pwm.PWM1A).read()))