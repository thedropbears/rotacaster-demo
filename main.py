from robot import Robot
from commands import Commands
from input import Input

def main():
    input = Input()
    robot = Robot()
    commands = Commands(robot, input)
    
    # keep the daemonising threads alive
    while True:
        pass

if __name__ == "__main__":
    main()