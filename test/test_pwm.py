"""Unit tests for PID submodule."""

import unittest
from pwm import Pwm
import tempfile, os

class PwmTest(unittest.TestCase):
    
    def setUp(self):
        tmpdir = tempfile.mkdtemp()
        # Create a temporary node tree
        self.PWM99A = tmpdir + "/sys/devices/ocp.3/pwm_test_P9_99"
        self.PWM99A_dir = self.PWM99A + '.12' # Device tree files have an incrementing .XX suffix
        Pwm.IDS.append(self.PWM99A)
        if not os.path.exists(self.PWM99A_dir):
            os.makedirs(self.PWM99A_dir)
    
    def test_pwm_init(self):
        p = Pwm(self.PWM99A)
        # Test default values
        self.assertEqual(p.pwm_id, self.PWM99A_dir)
        self.assertEqual(p.min_duty, 600000)
        self.assertEqual(p.max_duty, 2400000)
        self.assertEqual(p.period, 10000000)
        self.assertEqual(10000000, float(open(self.PWM99A_dir + Pwm.PERIOD).read()))
        # Test non-default values
        p = Pwm(self.PWM99A, 10000, 20000, 100000)
        self.assertEqual(p.min_duty, 10000)
        self.assertEqual(p.max_duty, 20000)
        self.assertEqual(p.period, 100000)
        self.assertEqual(100000, float(open(self.PWM99A_dir + Pwm.PERIOD).read()))
    
    def test_pwm_output(self):
        min = 10000
        max = 20000
        zero = (min + max)/2.0
        period = 100000
        p = Pwm(self.PWM99A, min, max, period) # Use round numbers to make things easier
        
        speed = p.set_speed(0)
        self.assertEqual(speed, zero)
        self.assertEqual(zero, float(open(self.PWM99A_dir + Pwm.DUTY).read()))
        speed = p.set_speed(0.5)
        self.assertEqual(speed, (max+zero)/2.0)
        self.assertEqual((max+zero)/2.0, float(open(self.PWM99A_dir + Pwm.DUTY).read()))
        speed = p.set_speed(-1.0)
        self.assertEqual(speed, min)
        self.assertEqual(min, float(open(self.PWM99A_dir + Pwm.DUTY).read()))
        speed = p.set_speed(1.0)
        self.assertEqual(speed, max)
        self.assertEqual(max, float(open(self.PWM99A_dir + Pwm.DUTY).read()))
