"""Unit tests for PID submodule."""

import unittest
from pid import Pid

class TestPid(unittest.TestCase):

    def test_init(self):
        p = Pid()
        self.assertNotEqual(p, None)
