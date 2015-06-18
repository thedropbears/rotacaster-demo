import threading
import socket, sys
import math

MPU_PORT = 4774

class Mpu(threading.Thread):
    
    def __init__(self):
        super(Mpu, self).__init__()
        self.euler = [0, 0, 0]
        self.gyro = [0, 0, 0]
        self.accel = [0, 0, 0]
        self.quat = [0, 0, 0, 0]
        self.yaw_offset = None
        self.raw_yaw = 0.0
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
            self.raw_yaw = self.euler[0]
            if self.yaw_offset == None:
                self.zero_yaw()
            self.euler[0] -= self.yaw_offset
            self.euler[0] = math.atan2(math.sin(self.euler[0]), math.cos(self.euler[0]))
            self.gyro = exploded[3:6]
            self.accel = exploded[6:9]
            self.quat = exploded[9:13]
    
    def zero_yaw(self):
        self.yaw_offset = self.raw_yaw
    
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
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.sock.bind(('', MPU_PORT)) # bind to all interfaces/addresses by default
        except socket.error, msg:
            sys.stderr.write("Error: Socket failed to bind %s\n" % msg[1])
    
    def get_euler(self):
        return self.euler
    
    def get_gyro(self):
        return self.gyro
    
    def get_accel(self):
        return self.accel
    
    def get_quat(self):
        return self.quat