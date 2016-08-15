import math, time

def drive(vX, vY, vZ, throttle, gyro, pwms):

    vX, vY = field_orient(vX, vY, gyro.get_yaw())

    # Drive equations that translate vX, vY and vZ into commands to be sent to the motors
    # front motor
    mA = -(((0.0 * vX) + (vY * 1.0)) / 2.0 + vZ / 3.0)
    # bottom left motor
    mB = (((-vX * math.sin(math.radians(60))) + (-vY / 2.0)) / 2.0 + vZ / 3.0)
    # bottom right motor
    mC = (((vX * math.sin(math.radians(60))) + (-vY / 2.0)) / 2.0 + vZ / 3.0)

    motor_input = [mA, mB, mC]

    max = max(max(abs(i) for i in motor_input), 1.0)

    # scale between -1 and 1, * by throttle, set speed
    for i in range(3):
        motor_input[i] /= max
        motor_input[i] *= throttle
        pwms[i].set_speed(motor_input[i])
    return drive


def field_orient(vX, vY, yaw_angle):
    oriented_vx = vX * math.cos(yaw_angle) + vY * math.sin(yaw_angle)
    oriented_vy = -vX * math.sin(yaw_angle) + vY * math.cos(yaw_angle)
    return oriented_vx, oriented_vy

def circle(gyro, pwms):
    while True:
        yield

def square(gyro, pwms):
    while True:
        yield
    FORWARD = [1.0, 0,0]
    RIGHT = [0.0, -1.0]
    BACK = [-1.0, 0.0]
    LEFT = [0.0, 1.0]
    order = [RIGHT, BACK, LEFT, FORWARD]
    SEGMENT_DURATION = 4
    CARTESIAN_SCALE = 0.5
    last_time = time.time()
    seg = 0
    if time.time - last_time > SEGMENT_DURATION/2.0:
        last_time = time.time()
    else:
        self.commands.robot.drive(1.0, 1.0, 0.0, self.CARTESIAN_SCALE)
        yield
