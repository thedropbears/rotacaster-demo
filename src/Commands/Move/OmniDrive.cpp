#include "OmniDrive.h"

OmniDrive::OmniDrive() : CommandBase("OmniDrive")
{
    // Use Requires() here to declare subsystem dependencies
    // eg.Requires(chassis);
    Requires(chassis);
}

// Called just before this Command runs the first time
void OmniDrive::Initialize()
{

}

// Called repeatedly when this Command is scheduled to run
void OmniDrive::Execute()
{
    // here we get the joystick's current state from OI
    // we reverse the axis so that forward and left are +ve
    // we also swap the x and y axis (by calling the opposite funcitons)
    double x = - oi->getJoyDrvY();
    double y = -oi->getJoyDrvX();
    double z = - oi->getJoyDrvZ();
    double throttle = oi->getJoyDrvThrottle();

    // here we call the chassis drive command to make the robot drive
    chassis->Drive(x, y, z, throttle);
}

// Make this return true when this Command no longer needs to run execute()
bool OmniDrive::IsFinished()
{
    return false;
}

// Called once after isFinished returns true
void OmniDrive::End()
{
    chassis->Drive(0.0,0.0,0.0,0.0);
}

// Called when another command which requires one or more of the same
// subsystems is scheduled to run
void OmniDrive::Interrupted()
{
    End();
}
