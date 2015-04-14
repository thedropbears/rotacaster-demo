#ifndef CHASSIS
#define CHASSIS

/* This is the chassis subsystem.
 * Often considered the "mother of all subsystems" the chassis
 * subsystem combines instructions from the driver (in teleop),
 * the PID loop and field centered driving to make the robot move.
 */

/*
 * A subsystem is an interface written by the programmer to control
 * the systems of the robot.
 * Subsystems are used by commands to provide a (hopefully)
 * easy to use interface to the lower level functions of
 * the robot and to keep all of the code directly controlling
 * one system in a single place.
 * Each subsystem monitors and controls a "system" on the robot
 * (such as the chassis subsystem controlling the real-life drive
 * system).
 */

#include "WPILib.h"

class Chassis: public Subsystem
{
private:
    CANTalon* motor_a;
    CANTalon* motor_b;
    CANTalon* motor_c;
    CANTalon *motors[3];
public:
    Chassis();
    ~Chassis();
    void Drive(double vX, double vY, double vZ, double throttle);
    void PutDashboard();
};

#endif
