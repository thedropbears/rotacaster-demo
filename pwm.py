import glob, os

class Pwm(object):
    PORTS = {
        "PWM0A-22": "/tmp/pwm/0A",
        "PWM0A-31": "/tmp/pwm/0A",
        "PWM0B-21": "/tmp/pwm/0B",
        "PWM0B-29": "/tmp/pwm/0B",
        "PWM1A-14": "/tmp/pwm/1A",
        "PWM1A-36": "/tmp/pwm/1A",
        "PWM1B-16": "/tmp/pwm/1B",
        "PWM1B-34": "/tmp/pwm/1B",
        "PWM2A-19": "/tmp/pwm/2A",
        "PWM2A-45": "/tmp/pwm/2A",
        "PWM2B-13": "/tmp/pwm/2B",
        "PWM2B-46": "/tmp/pwm/2B"}

    DUTY = "/duty_cycle" # the file that holds the current duty cycle in ns
    STATUS = "/enable" # the file that holds a 1 or a 0 telling the bbb weather to have pwm on or not
    PERIOD = "/period" # the file that holds the PWM period, in ns
        
    def __init__(self, pwm_id, min_duty = 1000000, max_duty = 2000000, period = 10000000):
        if not pwm_id in Pwm.PORTS.keys():
            raise Exception("Must pass in a recognised BBB PWM port: " + str(Pwm.PORTS.keys()))
        self.pwm_id = pwm_id
        self.pwm_dir = Pwm.PORTS[pwm_id]
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
        duty_in_ns = int(((speed+1.0)/2.0) * 
                         (self.max_duty - self.min_duty) + self.min_duty)
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
