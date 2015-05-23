class Pid(object):
    """Class to run a PID control loop."""
    def __init__(self, pid_output, kP, kI=0.0, kD=0.0, kF=0.0, set_point=0.0, izone=None):
        if not(isinstance(pid_output, PidOutput)):
            raise Exception("Must pass in a PidOutput object")
        self.kP=kP
        self.kI=kI
        self.kD=kD
        self.kF=kF
        self.last_error = 0.0
        self.integrator = 0.0
        self.output = pid_output
        self.set_point = set_point
        self.izone = izone
    
    def update(self,current_value):
        """Calculate PID output value for given reference input and feedback"""

        self.error = self.set_point - current_value

        self.p_value = self.kP * self.error
        self.d_value = self.kD * ( self.error - self.last_error)
        self.last_error = self.error
        
        #we add to the last i value so the error accumulates
        self.integrator += self.error
        
        if not self.izone == None: #the pythonic way
            if self.integrator > self.izone:
                self.integrator = self.izone
            elif self.integrator < -self.izone:
                self.integrator = -self.izone

        self.i_value = self.integrator * self.kI

        correction = self.p_value + self.i_value + self.d_value

        self.output.correction = correction
    
    def setPoint(self,set_point):
        """
        Initilize the setpoint of PID
        """
        self.set_point = set_point
        self.integrator=0
        self.last_derivator=0

    def setkP(self,P):
        self.kP=P

    def setkI(self,I):
        self.kI=I

    def setKd(self,D):
        self.Kd=D

    def getPoint(self):
        return self.set_point

    def getError(self):
        return self.error

class PidOutput(object):
    """Class that Pid objects output to."""
