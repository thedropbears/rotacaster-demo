from robot import Robot
from commands import Commands
from input import Input
from pwm import Pwm

def main():
    robot = Robot()
    input = Input(robot)
    commands = Commands(robot, input)
    
    # keep the daemonising threads alive
    while True:
        pass

if __name__ == "__main__":
    try:
        main()
    except Exception:
        pa = Pwm(Robot.MOTOR_A_PWM)
        pb = Pwm(Robot.MOTOR_B_PWM)
        pc = Pwm(Robot.MOTOR_C_PWM)
        pa.set_speed(0.0)
        pb.set_speed(0.0)
        pc.set_speed(0.0)
        print "Exception Thrown, all motors stopped"
    