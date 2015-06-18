import glob

class Qep(object):
    PORTS = {
        "QEP0" : "/sys/devices/ocp.3/48300000.epwmss/48300180.eqep",
        "QEP1" : "/sys/devices/ocp.3/48302000.epwmss/48302180.eqep",
        "QEP2" : "/sys/devices/ocp.3/48304000.epwmss/48304180.eqep" }
    
    # The counting mode of the encoder, 0=absolute, 1=relative
    MODE = "/mode"
    # The file for the period of the encoder -
    # or how long it takes for the timer for velocity to reset, in ns
    PERIOD = "/period"
    # The position of the encoder. In absolute mode this represents the current position;
    # in relative mode this represents its position at the last unit timer overflow
    POSITION = "/position"
    
    MODE_ABSOLUTE = 0
    MODE_RELATIVE = 1
    
    def __init__(self, qep_id, mode = MODE_ABSOLUTE, cpr = 180, period = 10000000, position = 0):
        if not qep_id in Qep.PORTS.keys():
            raise Exception("Must pass in a recognised BBB QEP port: " + str(Qep.PORTS.keys()))
        self.qep_id = qep_id
        self.qep_dir = glob.glob(Qep.PORTS[qep_id])[0]
        #self.qep_dir = Qep.PORTS[qep_id]
        if mode == Qep.MODE_RELATIVE and period <= 0:
            raise Exception("Must pass in a valid counting period greater than zero in relative mode")
        self.mode = mode
        self.write((self.qep_dir+Qep.MODE), str(self.mode))
        self.cpr = cpr
        self.period = period
        self.period_in_seconds = self.period / 1000000000.0
        # Write the period to a file
        if self.mode == Qep.MODE_RELATIVE:
            self.write((self.qep_dir+Qep.PERIOD), str(self.period))
        self.position = position
        self.write((self.qep_dir+Qep.POSITION), str(self.position))
        
    def get_revolutions(self):
        """Return the number of revolutions between here and the zero point as a float, with 1.0 being 1 revolution"""
        if self.mode == Qep.MODE_RELATIVE:
            raise Exception("Number of absolute revolutions is unavailable in velocity mode. Try Qep.getSpeed() instead")
        return -(float(open(self.qep_dir+Qep.POSITION).read()))#/4.0/self.cpr)
    
    def get_speed(self):
        """Return the scpeed of the encoder in relative mode in revolutions per second"""
        if self.mode == Qep.MODE_ABSOLUTE:
            raise Exception("Speed of wheel is unavailable in absolute mode. Try Qep.getRevolutions() instead")
        return -(float(open(self.qep_dir+Qep.POSITION).read())/self.period_in_seconds)
    
    def get_raw_speed(self):
        """Return the speed of the encoder in relative mode in revolutions per period"""
        if self.mode == Qep.MODE_ABSOLUTE:
            raise Exception("Speed of wheel is unavailable in absolute mode. Try Qep.getRevolutions() instead")
        return -(float(open(self.qep_dir+Qep.POSITION).read()))
    
    def set_position(self, position):
        self.write(self.qep_dir+self.POSITION, str(position))
    
    def write(self, path, data):
        """Overwrites or creates file at path and writes data to it"""
        f = open(path, "w")
        f.write(data)
        f.close()
        
    