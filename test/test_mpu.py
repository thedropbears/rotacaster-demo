"""Unit tests for mpu submodule"""

import unittest
import time
from socket import *
from mpu import Mpu

MPU_PORT = 4774

s = socket(AF_INET, SOCK_DGRAM)

class TestMpu(unittest.TestCase):
    def test_udp_receiver(self):
        """Test that the mpu submodule is able to pick up and interpret packets in the correct format"""
        mpu = Mpu()
        
        time.sleep(0.5)
        
        s.sendto("0,1,2,3,4,5,6,7,8,9,10,11,12", ("127.0.0.1", MPU_PORT))
        
        time.sleep(1)
        
        self.assertEqual(mpu.get_euler(), [0, 1, 2])
        self.assertEqual(mpu.get_gyro(), [3, 4, 5])
        self.assertEqual(mpu.get_accel(), [6, 7, 8])
        self.assertEqual(mpu.get_quat(), [9, 10, 11, 12])
        
        mpu.stop_monitoring()
        """Unit tests for mpu submodule"""

import unittest
import time
from socket import *
from mpu import Mpu

MPU_PORT = 4774

s = socket(AF_INET, SOCK_DGRAM)

class TestMpu(unittest.TestCase):
    def test_udp_receiver(self):
        """Test that the mpu submodule is able to pick up and interpret packets in the correct format"""
        mpu = Mpu()
        
        time.sleep(0.1)
        
        s.sendto("0,1,2,3,4,5,6,7,8,9,10,11,12", ("127.0.0.1", MPU_PORT))
        
        time.sleep(0.1)
        
        self.assertEqual(mpu.getEuler(), [0, 1, 2])
        self.assertEqual(mpu.getGyro(), [3, 4, 5])
        self.assertEqual(mpu.getAccel(), [6, 7, 8])
        self.assertEqual(mpu.getQuat(), [9, 10, 11, 12])
        
        mpu.stop_monitoring()