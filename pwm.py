PWM1A = "/sys/devices/ocp.3/pwm_test_P9_14" # the directory where the files to set for pwm output 1a are held
IDS = [PWM1A] # a list of all pwm ids for the pwm object to check against to ensure that we are passed a real directory
DUTY = "/duty" # the file that holds the current duty cycle in ns
STATUS = "/run" # the file that holds a 1 or a 0 telling the bbb weather to have pwm on or not
PERIOD = "/period" # the file that holds the PWM period, in ns

import glob

class Pwm(object):
        
    def __init__(self, pwm_id, min_duty = 600000, max_duty = 2400000, period = 10000000):
        if not pwm_id in IDS:
            raise Exception("Must pass in a path to a BBB pwm file (see pwm.IDS)")
        self.pwm_id = glob.glob(pwm_id + '.*')[0]
        self.min_duty = min_duty
        self.max_duty = max_duty
        self.period = period
        self.write((self.pwm_id+PERIOD), str(period))
        self.set_speed(0.0) # set our speed to 0 before turning pwm no
        self.pwm_on()
        
    def set_speed(self, speed):
        if not -1 <= speed <= 1:
            raise Exception("Speed must be passed as a float between -1 and 1")
        # convert speed from float from 0 to 1 into a time in ns
        duty_in_ns = ((speed+1.0)/2.0) * (self.max_duty - self.min_duty) + self.min_duty
        self.write(self.pwm_id + DUTY, str(duty_in_ns))
        return duty_in_ns
    
    def write(self, path, data):
        """Overwrites or creates file at path and writes data to it"""
        f = open(path, "w")
        f.write(data)
        f.close()
        
    def pwm_on(self):
        self.write((self.pwm_id+STATUS), "1")
    
    def pwm_off(self):
        self.write((self.pwm_id+STATUS), "0")
