#include "Robot.h"
#include "Commands/Command.h"
#include "Commands/ExampleCommand.h"
#include <lib-4774/Functions.h>

void Robot::RobotInit()
{
    CommandBase::init();
    autonomousCommand = new ExampleCommand();
    lw = LiveWindow::GetInstance();
}

void Robot::DisabledPeriodic()
{
    Scheduler::GetInstance()->Run();
}

void Robot::AutonomousInit()
{
    if (autonomousCommand != NULL)
        autonomousCommand->Start();
}

void Robot::AutonomousPeriodic()
{
    Scheduler::GetInstance()->Run();
}

void Robot::TeleopInit()
{
    // This makes sure that the autonomous stops running when
    // teleop starts running. If you want the autonomous to
    // continue until interrupted by another command, remove
    // this line or comment it out.
    if (autonomousCommand != NULL)
        autonomousCommand->Cancel();
}

void Robot::TeleopPeriodic()
{
    Scheduler::GetInstance()->Run();
}

void Robot::TestPeriodic()
{
    lw->Run();
}

void Robot::PutDashboard() {
    SmartDashboard::PutNumber("Roll (Deg)", lib4774::r2d(CommandBase::imu->GetRoll()));
    SmartDashboard::PutNumber("Pitch (Deg)", lib4774::r2d(CommandBase::imu->GetPitch() ));
    SmartDashboard::PutNumber("Yaw (Deg)", lib4774::r2d(CommandBase::imu->GetYaw()));

}

START_ROBOT_CLASS(Robot);

