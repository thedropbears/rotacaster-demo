#include "Chassis.h"
#include <RobotMap.h>

// These are the gains for the velocity PID on the wheels
// this means that no matter what load the robot's wheels
// are taking. this system works by using encoders on the
// wheels to find out their speed and then correcting that
// using this pid controller (which is built in to the talons).
// may need to make these negative
// need to check on real robot...
const int VEL_P = 0.0;
const int VEL_I = 3.0;
const int VEL_D = 0.0;
const int VEL_F = 2.0;
const int VEL_CONTROL_PROFILE = 0;

Chassis::Chassis() : Subsystem("Chassis") {
    // here we are initialising all of the motors with the CAN IDs
    // defined in robotmap and putting them in an array
    motors[0] = new CANTalon(DRIVE_MOTOR_A_ID);
    motors[1] = new CANTalon(DRIVE_MOTOR_B_ID);
    motors[2] = new CANTalon(DRIVE_MOTOR_C_ID);

    // here we are configuring the velocity PID on the talons
    // using the constants defined above
    for(int i = 0; i < 3; i++) {
        // setting it to speed control mode
        motors[i]->SetControlMode(CANTalon::ControlMode::kSpeed);
        // what profile slot these settings are saved in (there are two slots)
        motors[i]->SelectProfileSlot(VEL_CONTROL_PROFILE);
        // setting the gains for the actual PID loop
        motors[i]->SetPID(VEL_P, VEL_I, VEL_D, VEL_F);
        // making sure that the I is not capped (sometimes we want to do this
        // to stop too much integrator windup)
        motors[i]->SetIzone(0);
        // making sure that the ramp rate on the wheels is not capped
        motors[i]->SetCloseLoopRampRate(0);
    }

}

Chassis::~Chassis() {
    // delete all of the motors from memory
    for(int i = 0; i < 3; i++) {
        delete motors[i];
    }
}

void Chassis::Drive(double vX, double vY, double vZ, double throttle) {
    // virtual motor speeds that are operated on to find out the
    // speed the motors should be commanded to go at
    double mA;
    double mB;
    double mC;

    // field orient etc here

    // placeholders for motor equations
    mA = 0.0;
    mB = 0.0;
    mC = 0.0;


}
