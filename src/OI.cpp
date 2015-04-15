#include "OI.h"
#include <lib-4774/Functions.h>
#include <RobotMap.h>

#include <Commands/Gyro/ResetGyro.h>
#include <Commands/Gyro/ToggleFieldDrive.h>
#include <Commands/Gyro/TogglePID.h>

OI::OI()
{
    // initializing the joystick class to be device 0
    // (you can have multiple devices plugged into your
    // driver station
    JoyDrv = new Joystick(0);
    // Process operator interface input here.

    gyroResetButton = new JoystickButton (JoyDrv, GYRO_RESET_BUTTON);
    gyroResetButton->WhenPressed(new ResetGyro());

    fieldOrientButton = new JoystickButton (JoyDrv, FIELD_ORIENT_BUTTON);
    fieldOrientButton->WhenPressed(new ToggleFieldDrive());

    togglePIDButton = new JoystickButton (JoyDrv, TOGGLE_PID_BUTTON);
    togglePIDButton->WhenPressed(new TogglePID());
}

Joystick* OI::getJoyDrv() {
    return JoyDrv;
}

double OI::getJoyDrvX(){
    // here we use the lib-4774 scaling functions to scale the joystick's x axis
    // the joystick's x axis is left and right (but the robot's x and yare swapped)
    float scaled = lib4774::scaleJoystick(JoyDrv->GetX(), JOYSTICK_X_EXPONENTIAL, JOY_DRV_DEAD_X, JOYSTICK_X_SCALE);
    return scaled;
}

double OI::getJoyDrvY(){
    // here we use the lib-4774 scaling functions to scale the joystick's y axis
    // the joystick's y axis is forward and back (but the robot's x and y are swapped)
    float scaled = lib4774::scaleJoystick(JoyDrv->GetY(), JOYSTICK_Y_EXPONENTIAL, JOY_DRV_DEAD_Y, JOYSTICK_Y_SCALE);
    return scaled;
}

double OI::getJoyDrvZ(){
    // here we use the lib-4774 scaling functions to scale the joystick's z axis
    // the joystick's z axis is its twist
    float scaled = lib4774::scaleJoystick(JoyDrv->GetZ(), JOYSTICK_Z_EXPONENTIAL, JOY_DRV_DEAD_Z, JOYSTICK_Z_SCALE);
    return scaled;
}

double OI::getJoyDrvThrottle(){
    // here we take the joystick's throttle and scale it so it is between 0 and 1
    return (JoyDrv->GetThrottle()-1.0)/-2.0;
}
