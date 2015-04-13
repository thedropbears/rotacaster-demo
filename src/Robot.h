#include "WPILib.h"
#include "CommandBase.h"

class Robot: public IterativeRobot {
private:
    Command *autonomousCommand;
    LiveWindow *lw;

    // function that is called when the robot code first starts
    // (e.g. upon roboRIO bootup or robot code reset)
    // it is usually used to initialize commands and
    // to start the command base (the object that handles all of the subsystems)
    void RobotInit();

    // function that is called at 50 Hz (or slower depending on how much
    // of a load the roboRIO is under) while the robot disabled
    // there is no set use for this function, but it can be used for
    // periodically "zeroing" or resetting systems such as a PID loop while they
    // are known to be inactive
    void DisabledPeriodic();

    // function that is called at the start of the autonomous period
    // it is used to start the robot's autonomous command (and in
    // some cases choose from a variety of autonomous commands)
    void AutonomousInit();

    // function that is called periodically while the robot is enabled in autonomous mode.
    // it is used by the robot code to schedule commands while the robot is in autonomous mode and
    // can be used by the programmer to put diagnostics to the SmartDashboard
    void AutonomousPeriodic();

    // function that is called at the beginning of teleop. it is used to
    // cancel the autonomous command, and in some cases set systems to be
    // ready for teleop
    void TeleopInit();

    // function that is called periodically while the robot is enabled in teleop mode.
    // it is used by the robot code to schedule commands while the robot is in teleop mode and
    // can be used by the programmer to put diagnostics to the SmartDashboard
    void TeleopPeriodic();

    // function that is called periodically while the robot is enabled in test mode.
    void TestPeriodic();
public:
    // function to put the latest robot data (that is in the body of the function)
    // to the dashboard
    void PutDashboard();
};
