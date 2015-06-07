"""Unit tests for the Qep submodule"""

import unittest
from qep import Qep
import tempfile, os


class QepTest(unittest.TestCase):
    
    def setUp(self):
        tmpdir = tempfile.mkdtemp()
        # Create a temporary node tree
        self.QEP99 = tmpdir + "/sys/devices/ocp.2/48306000.epwmss/48306180.eqep"
        self.QEP99_dir = self.QEP99
        Qep.PORTS["QEP99"] = self.QEP99
        if not os.path.exists(self.QEP99_dir):
            os.makedirs(self.QEP99_dir)
        
    def set_qep_count(self, position):
        # Open the mode attribute file
        position_file = open(self.QEP99 + Qep.POSITION, "w")
        
        # Write the desired position into the file
        position_file.write(str(position))
        position_file.close()
        
    def read_file(self, path):
        file = open(path, "r")
        data = file.read()
        file.close()
        return data
        
    def test_qep_init(self):
        # Test default values
        q = Qep("QEP99")
        # Ensure that the qep's *ID* is being set
        self.assertEqual(q.qep_id, "QEP99")
        # Ensure that qep is correctly turning the id into a file
        self.assertEqual(q.qep_dir, self.QEP99)
        # Ensure that the encoder is in relative mode, as commanded
        self.assertEqual(Qep.MODE_ABSOLUTE, int(open(self.QEP99_dir+Qep.MODE).read()))
        # Ensure that we are zeroing the encoder file value
        self.assertEqual(0.0, float(open(self.QEP99_dir+Qep.POSITION).read()))
        
        # Test non default values
        #          ID        Counting Mode    Counts per Rev.   Period   Position
        q = Qep("QEP99", Qep.MODE_RELATIVE,     360,           100000000,   720)
        # Ensure that we are setting the right mode
        self.assertEqual(Qep.MODE_RELATIVE, int(open(self.QEP99_dir+Qep.MODE).read()))
        # Ensure that we are setting the correct counts per rev
        self.assertEqual(360, q.cpr)
        # Ensure that we are setting the period
        self.assertEqual(100000000, float(open(self.QEP99_dir+Qep.PERIOD).read()))
        # Ensure that we are setting the position
        self.assertEqual(720, float(open(self.QEP99_dir+Qep.POSITION).read()))
        
    def test_qep_output(self):
        # Absolute Mode Tests
        q = Qep("QEP99")
        
        # Test that we are quad counting and scaling the values correctly
        self.set_qep_count(360)
        self.assertEqual(0.5, q.get_revolutions())
        self.set_qep_count(720)
        self.assertEqual(1.0, q.get_revolutions())
        
        # Test non default values
        q = Qep("QEP99", cpr = 100, position = 200)
        self.assertEqual(0.5, q.get_revolutions())
        self.set_qep_count(400)
        self.assertEqual(1.0, q.get_revolutions())
        
        # Relative/Velocity mode tests
        q = Qep("QEP99", Qep.MODE_RELATIVE)
        
        # Test that we get the correct speed; default value is 100 overflows per second
        self.set_qep_count(1.0)
        self.assertEqual(100.0, q.get_speed()) # represents revolutions per second
        self.assertEqual(1.0, q.get_raw_speed()) # represents revolutions per period
        self.set_qep_count(0.5)
        self.assertEqual(50.0, q.get_speed()) # represents revolutions per second
        self.assertEqual(0.5, q.get_raw_speed()) # represents revolutions per period
        
        # Test non-default values
        q = Qep("QEP99", Qep.MODE_RELATIVE, period = 20000000)
        self.set_qep_count(1.0)
        self.assertEqual(50.0, q.get_speed())
        self.assertEqual(1.0, q.get_raw_speed())
        self.set_qep_count(0.5)
        self.assertEqual(25.0, q.get_speed())
        self.assertEqual(0.5, q.get_raw_speed())