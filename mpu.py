import threading
from socket import socket, AF_INET, SOCK_DGRAM

MPU_PORT = 4774

class Mpu(threading.Thread):
    
    def __init__(self):
        super(Mpu, self).__init__()
        self.euler = [0, 0, 0]
        self.gyro = [0, 0, 0]
        self.accel = [0, 0, 0]
        self.quat = [0, 0, 0, 0]
        self.sock = False
        self.running = threading.Event()
        self.running.set()
        self.daemon = True
        self.start()
    
    def run(self):
        self.monitor_udp()
    
    def monitor_udp(self):
        while self.running.isSet():
            exploded = self.get_data()
            self.euler = exploded[:3]
            self.gyro = exploded[3:6]
            self.accel = exploded[6:9]
            self.quat = exploded[9:13]
    
    def stop_monitoring(self):
        """Essentially destroys the new thread to stop looping for infinity"""
        self.running.clear()
    
    def get_data(self):
        if not self.sock:
            self.make_sock()
        packet = self.sock.recv(1024)
        exploded = [float(val) for val in packet.split(',')]
        return exploded
    
    def make_sock(self):
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.bind(('', MPU_PORT)) # bind to all interfaces/addresses by default
    
    def getEuler(self):
        return self.euler
    
    def getGyro(self):
        return self.gyro
    
    def getAccel(self):
        return self.accel
    
    def getQuat(self):
        return self.quat