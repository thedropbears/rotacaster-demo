"""Unit tests for mpu submodule"""

import unittest
import sys
from socket import *
from mpu import Mpu

MPU_PORT = 4774

s = socket(AF_INET, SOCK_DGRAM)

class TestMpu(unittest.TestCase):
    def test_udp_receiver(self):
        """Test that the mpu submodule is able to pick up and interpret packets in the correct format"""
        mpu = Mpu()
        s.sendto("0,1,2,3,4,5,6,7,8,9,10,11,12", ("127.0.0.1", MPU_PORT))
        
        assertEqual(mpu.getEuler(), [0, 1, 2])