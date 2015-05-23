class Pid(object):
    """Class to run a PID control loop."""
    def __init__(self, pid_output, kP, kI=0.0, kD=0.0, kF=0.0):
        self.kP=kP
        self.kI=kI
        self.kD=kD
        self.kF=kF
        if not(isinstance(pid_output, PidOutput)):
            raise Exception("Must pass in a PidOutput object")
        return kP


class PidOutput(object):
    """Class that Pid objects output to."""
    def __init__(self):
        pass