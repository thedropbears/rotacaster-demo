"""Unit tests for PID submodule."""

import unittest
from pid import Pid, PidOutput

class PidOutputTest(PidOutput):
    def set(self, value):
        self.correction = value

class TestPid(unittest.TestCase):

    def test_init_pidoutput(self):
        """Check that Pid class only accepts PidOutputs in the constructor."""
        with self.assertRaises(Exception):
            p = Pid(object(), 0.0)

    def test_init_constants(self):
        """Check that the PID constants are set properly."""
        output = PidOutputTest()
        p = Pid(output, 1.0)
        self.assertEqual(p.kP, 1.0)
        self.assertEqual(p.kI, 0.0)
        self.assertEqual(p.kD, 0.0)
        self.assertEqual(p.kF, 0.0)
        self.assertEqual(p.output, output)

        p = Pid(output, 1.0, 2.0, 3.0, 4.0)
        self.assertEqual(p.kP, 1.0)
        self.assertEqual(p.kI, 2.0)
        self.assertEqual(p.kD, 3.0)
        self.assertEqual(p.kF, 4.0)
    
    def test_pid_update(self):
        #baseline test
        output = PidOutputTest()
        p = Pid(output, 0.0)
        p.setPoint(0.0)
        p.update(0)
        self.assertEqual(output.correction, 0)
        p.update(100)
        self.assertEqual(output.correction, 0)
        
        #test kp is working
        p = Pid(output, 1.0)
        p.update(0)
        self.assertEqual(output.correction, 0)
        p.update(100)
        self.assertEqual(output.correction, 1.0*-100)
        p.update(0)
        self.assertEqual(output.correction, 0)
        
        #test ki is working
        p = Pid(output, 0.0, 1.0)
        p.update(0)
        self.assertEqual(output.correction, 0)
        p.update(100)
        p.update(50)
        self.assertEqual(output.correction, 1.0*-150)
        p.update(-150)
        self.assertEqual(output.correction, 0)
        
        #test izone
        p = Pid(output, 0.0, 1.0, izone=100)
        p.update(0)
        self.assertEqual(output.correction, 0)
        p.update(100)
        p.update(50)
        self.assertEqual(output.correction, 1.0*-100)
        p.update(-100)
        self.assertEqual(output.correction, 0)
        p.update(0)
        self.assertEqual(output.correction, 0)
        p.update(-100)
        p.update(-50)
        self.assertEqual(output.correction, 1.0*100)
        p.update(100)
        self.assertEqual(output.correction, 0)
        
        #test kd is working
        p = Pid(output, 0.0, 0.0, 1.0)
        p.update(0)
        self.assertEqual(output.correction, 0)
        p.update(100)
        self.assertEqual(output.correction, -100)
        p.update(0)
        self.assertEqual(output.correction, 100)
        p.update(0)
        self.assertEqual(output.correction, 0)
        