"""Unit tests for PID submodule."""

import unittest
from pid import Pid, PidOutput

class TestPid(unittest.TestCase):

    def test_init_return(self):
        p = Pid(1, PidOutput())
        self.assertNotEqual(p, None)