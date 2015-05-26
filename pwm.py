class Pwm(object):
    PWM1A = "/sys/devices/ocp.3/pwm_test_P9_14" # the directory where the files to set for pwm output 1a are held
    IDS = [PWM1A] # a list of all pwm ids for the pwm object to check against to ensure that we are passed a real directory
    DUTY = "/duty" # the file that holds the current duty cycle in ns
    STATUS = "/run" # the file that holds a 1 or a 0 telling the bbb weather to have pwm on or not
    FULL_BACK_DUTY = 600000 # nanoseconds
    ZERO_DUTY = 1500000 #nanoseconds
    FULL_DUTY = 2400000 #nanoseconds
    ZERO_TO_FULL = (FULL_DUTY - FULL_BACK_DUTY)/2
        
    def __init__(self, pwm_id):
        if not pwm_id in self.IDS:
            raise Exception("Must pass in a path to a BBB pwm file (see pwm.IDS)")
        self.pwm_id = pwm_id
        self.set_speed(0.0) # set our speed to 0 before turning pwm no
        self.pwm_on()
        
    def set_speed(self, speed):
        if not -1 <= speed <= 1:
            raise Exception("Speed must be passed as a float between -1 and 1")
        # convert speed from float from 0 to 1 into a time in ns
        duty_in_ns = (speed * self.ZERO_TO_FULL) + self.ZERO_TO_FULL + self.FULL_BACK_DUTY
        self.write(self.pwm_id+self.DUTY, str(duty_in_ns))
        return duty_in_ns
    
    def write(self, path, data):
        """Overwrites or creates file at path and writes data to it"""
        f = open(path, "w")
        f.write(data)
        f.close()
        
    def pwm_on(self):
        self.write((self.pwm_id+self.STATUS), "1")
    
    def pwm_off(self):
        self.write((self.pwm_id+self.STATUS), "0")