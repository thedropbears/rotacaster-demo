import glob

class Qep(object):
    PORTS = {
        "QEP1" : "/sys/devices/ocp.2/48300000.epwmss/48300180.eqep",
        "QEP2" : "/sys/devices/ocp.2/48302000.epwmss/48302180.eqep",
        "QEP3" : "/sys/devices/ocp.2/48304000.epwmss/48304180.eqep" }
    
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
    
    def __init__(self, qep_id, mode = MODE_ABSOLUTE, cpr = 180, period = 100000000, position = 0):
        if not qep_id in Qep.PORTS.keys():
            raise Exception("Must pass in a recognised BBB QEP port: " + str(Qep.PORTS.keys()))
        self.qep_id = qep_id
        self.qep_dir = glob.glob(Qep.PORTS[qep_id])[0]
        #self.qep_dir = Qep.PORTS[qep_id]
        if mode == Qep.MODE_RELATIVE and period <= 0:
            raise Exception("Must pass in a valid counting period greater than zero in relative mode")
        self.mode = mode
        self.write((self.qep_dir+self.MODE), str(self.mode))
        self.cpr = cpr
        self.period = period
        # Write the period to a file
        if self.mode == Qep.MODE_RELATIVE:
            self.write((self.qep_dir+self.PERIOD), str(self.period))
        self.position = position
        self.write((self.qep_dir+self.POSITION), str(self.position))
            
    def write(self, path, data):
        """Overwrites or creates file at path and writes data to it"""
        f = open(path, "w")
        f.write(data)
        f.close()
        
    