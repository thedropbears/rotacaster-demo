"""Unit tests for PID submodule."""

import unittest
from pid import Pid, PidOutput

class TestPid(unittest.TestCase):

    def test_init_pidoutput(self):
        """Check that Pid class only accepts PidOutputs in the constructor."""
        with self.assertRaises(Exception):
            p = Pid(object(), 0.0)

    def test_init_constants(self):
        """Check that the PID constants are set properly."""
        output = PidOutput()
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

