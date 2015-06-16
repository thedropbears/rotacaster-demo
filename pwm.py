import glob, os

class Pwm(object):
    PORTS = {
        "PWM0A-22": "/sys/devices/ocp.3/pwm_test_P9_22",
        "PWM0A-31": "/sys/devices/ocp.3/pwm_test_P9_31",
        "PWM0B-21": "/sys/devices/ocp.3/pwm_test_P9_21",
        "PWM0B-29": "/sys/devices/ocp.3/pwm_test_P9_29",
        "PWM1A-14": "/sys/devices/ocp.3/pwm_test_P9_14",
        "PWM1A-36": "/sys/devices/ocp.3/pwm_test_P8_36",
        "PWM1B-16": "/sys/devices/ocp.3/pwm_test_P9_16",
        "PWM1B-34": "/sys/devices/ocp.3/pwm_test_P8_34",
        "PWM2A-19": "/sys/devices/ocp.3/pwm_test_P8_19",
        "PWM2A-45": "/sys/devices/ocp.3/pwm_test_P8_45",
        "PWM2B-13": "/sys/devices/ocp.3/pwm_test_P8_13",
        "PWM2B-46": "/sys/devices/ocp.3/pwm_test_P8_46"}

    DUTY = "/duty" # the file that holds the current duty cycle in ns
    STATUS = "/run" # the file that holds a 1 or a 0 telling the bbb weather to have pwm on or not
    PERIOD = "/period" # the file that holds the PWM period, in ns
        
    def __init__(self, pwm_id, min_duty = 1000000, max_duty = 2000000, period = 10000000):
        if not pwm_id in Pwm.PORTS.keys():
            raise Exception("Must pass in a recognised BBB PWM port: " + str(Pwm.PORTS.keys()))
        self.pwm_id = pwm_id
        self.pwm_dir = glob.glob(Pwm.PORTS[pwm_id] + '.*')[0]
        self.min_duty = min_duty
        self.max_duty = max_duty
        self.period = period
        self.write((self.pwm_dir + Pwm.PERIOD), str(period))
        self.set_speed(0.0) # set our speed to 0 before turning pwm no
        self.pwm_on()
        
    def set_speed(self, speed):
        if speed >= 1.0:
            speed = 1.0
        if speed <= -1.0:
            speed = -1.0
        speed = -speed
        # convert speed from float from 0 to 1 into a time in ns
        duty_in_ns = self.period - int(((speed+1.0)/2.0) * (self.max_duty - self.min_duty) + self.min_duty)
        self.write(self.pwm_dir + Pwm.DUTY, str(duty_in_ns))
        return duty_in_ns
    
    def write(self, path, data):
        """Overwrites or creates file at path and writes data to it"""
        f = open(path, "w")
        f.write(data)
        f.close()
        
    def pwm_on(self):
        self.write((self.pwm_dir + Pwm.STATUS), "1")
    
    def pwm_off(self):
        self.write((self.pwm_dir + Pwm.STATUS), "0")
