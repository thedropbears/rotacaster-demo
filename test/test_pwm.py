"""Unit tests for PID submodule."""

import unittest
from pwm import Pwm
import tempfile, os

class PwmTest(unittest.TestCase):
    
    def setUp(self):
        tmpdir = tempfile.mkdtemp()
        os.chroot(tmpdir)
        
        if not os.path.exists(Pwm.PWM1A):
            os.makedirs(Pwm.PWM1A)
    
    def test_pwm_output(self):
                
        pwm = Pwm(Pwm.PWM1A)
        self.assertEqual(pwm.pwm_id, pwm.PWM1A)
        
        speed = pwm.set_speed(0)
        self.assertEqual(speed, Pwm.ZERO_DUTY)
        self.assertEqual(speed, float(open(Pwm.PWM1A+Pwm.DUTY).read()))
        speed = pwm.set_speed(0.5)
        self.assertEqual(speed, Pwm.ZERO_DUTY+(Pwm.ZERO_TO_FULL/2))
        self.assertEqual(speed, float(open(Pwm.PWM1A+Pwm.DUTY).read()))
        speed = pwm.set_speed(-1.0)
        self.assertEqual(speed, Pwm.FULL_BACK_DUTY)
        self.assertEqual(speed, float(open(Pwm.PWM1A+Pwm.DUTY).read()))
        speed = pwm.set_speed(1.0)
        self.assertEqual(speed, pwm.FULL_DUTY)
        self.assertEqual(speed, float(open(Pwm.PWM1A+Pwm.DUTY).read()))