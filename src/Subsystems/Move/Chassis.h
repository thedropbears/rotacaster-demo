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

#include <Subsystems/PID/GyroCorrection.h>

class Chassis: public Subsystem
{
private:
    // virtual representation of the motors. can be commanded to go to
    // specific speeds based on encoder values
    CANTalon* motor_a;
    CANTalon* motor_b;
    CANTalon* motor_c;
    CANTalon *motors[3];

    GyroCorrection *correction;
    PIDController *gyro_pid;
    // represents weather or not the PID correction is put to the wheels
    // (also if it is not setpoint is reset to the current heading)
    bool pidInControl;
    // are control inputs field oriented
    bool fieldOriented;

public:
    Chassis();
    ~Chassis();
    // the function that all commands call if they want the robot to drive
    // it takes in the desired motor values, scales these and combines them
    // with field orientation (if it is on) and pid (if it is on)
    void Drive(double vX, double vY, double vZ, double throttle);
    // put internal data to the smart dashboard
    void PutDashboard();
    // turn fieldorientation on or off
    void ToggleFieldOrient();
    // set the current heading to a different heading (relative to
    // gyro zero)
    void SetHeading(double newHeading);
    //change the current heading by change (relative to the current heading
    void HeadingChange(double change);
    // enable the PID controller (turn off PID)
    void EnablePID();
    // disable the pid controller (turn on PID)
    void DisablePID();
    // returns true when the pid loop brings us to the setpoint (within
    // a threshold)
    bool OnTarget();
    // returns true if the PID is on
    bool PIDEnabled();
    // distance in centimeters since encoders were last zeroed
    void EncoderDistance(double*);
    // zero the encoders
    void ZeroEncoders();
};

#endif
