import threading

class Mpu(threading.Thread):
    def run(self):
        monitor_udp()