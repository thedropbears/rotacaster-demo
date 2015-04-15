#include "Chassis.h"
#include <RobotMap.h>
#include <lib-4774/Functions.h>
#include <CommandBase.h>
#include <math.h>
#include <Commands/Move/OmniDrive.h>

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

// These are the gains for the heading pid. This means that
// if the robot is rotated without command, it  will automatically
// correct it's heading. It also means that when the robot
// is moving in a direction it will stay moving in a straight
// line.
const double YAW_P = 0.5;
const double YAW_I = 0.0;
const double YAW_D = 0.0;
// make sure that PID does not kick in when the chassis' momentum
// is too high to prevent it oscillating around a setpoint that was
// set too soon after rotation
const double YAW_MOMENTUM_THRESHOLD (lib4774::d2r(10.0)); //deg/s

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

    // the class that the PIDController output's it's output to
    correction = new GyroCorrection();
    // the class that does the magic of the PID
    gyro_pid = new PIDController(YAW_P, YAW_I, YAW_D, CommandBase::imu, correction);
    // as the pid takes input in radians, we set the input range to
    // PI radians each way (which is equal to 180 deg)
    gyro_pid->SetInputRange(-M_PI, M_PI);
    // this tells the controller that +PI is equal to -PI
    gyro_pid->SetContinuous(true);
    // set the setpoint to 0.0
    gyro_pid->SetSetpoint(0.0);
    // enable the controller
    gyro_pid->Enable();


    // field orient by default
    fieldOriented = true;
    // pid not in control by default (enabled but correction not put to the wheels)
    pidInControl = false;
}

Chassis::~Chassis() {
    // delete all of the motors from memory
    for(int i = 0; i < 3; i++) {
        delete motors[i];
    }
}

void Chassis::InitDefaultCommand() {
    // here we set the default command for the chassis subsystem
    // to omni drive, the command that lets the driver control the
    // robot
    SetDefaultCommand(new OmniDrive());
}

void Chassis::Drive(double vX, double vY, double vZ, double throttle) {
    // virtual motor speeds that are operated on to find out the
    // speed the motors should be commanded to go at
    double mA;
    double mB;
    double mC;
    double vPID = 0.0;

    // if field orientation is enabled
    if(fieldOriented) {
        // temporary array for fieldorient to act on
        double result[2] = {0, 0};
        // here we call lib-4774's fieldOrient function, which makes all inputs
        // to drive be relative to the last place the gyro was reset/zeroed
        lib4774::fieldOrient(vX, vY, CommandBase::imu->GetYaw(), result);
        vX = result[0];
        vY = result[1];
    }

    // if the PID is not disabled
    if(gyro_pid->IsEnabled()) {
        if (vZ != 0) {
            // we are spinning under command, so dont let pid take control
            pidInControl = false;
        } else if (abs(CommandBase::imu->GetZGyro()) < YAW_MOMENTUM_THRESHOLD) {
            // the momentum is less than the threshold and we are not under command
            //so PID can take control
            pidInControl = true;
        }

        if (pidInControl) {
            vPID = correction->correction;
        } else {
            // pid should not be in control, so we do not set vPID
            // to correction correction, but instead reset the PID
            // the current robot yaw
            double SetHeading = CommandBase::imu->GetYaw();
            // reset (temporarily disable) the gyro PID
            gyro_pid->Reset();
            // set the setpoint to the current heading so the correction is 0
            gyro_pid->SetSetpoint(SetHeading);
            // enable the pid
            gyro_pid->Enable();
            // set the correction to 0 so that the next time the code in the if
            // runs the previous value for correction is not still there
            correction->correction = 0;
        }

    }

    // placeholders for motor equations
    mA = 0.0;
    mB = 0.0;
    mC = 0.0;

    double motorInput [] = {mA, mB, mC};

    double max = 1;

    // motor scaling. here we scale all of the motor values to between + and - 1
    for (int i = 0; i < 3; i += 1)
    {
        // abs = absolute value (eg abs(-3.4) -> 3.4)
        if (abs(motorInput[i]) > max)
        {
            max = abs(motorInput[i]);
        }
    }

    for (int i =0; i < 3; i += 1)
    {
        // divide the motor inputs by the max value to scale between
        // + and - 1
        motorInput[i] = motorInput[i]/max;
    }

    for (int i =0; i < 3; i += 1)
    {
        // multiply by throttle (0 <= throttle <= 1)
        motorInput[i] = motorInput[i] * throttle;

    }

    if(gyro_pid->IsEnabled()) {
        // if the PID is enabled, we add vPID and do the scaling again with that
        max = 1;

        for (int i =0; i < 3; i += 1) {
            motorInput[i] -= vPID;
            if (abs(motorInput[i]) > max)
            {
                max = abs(motorInput[i]);
            }
        }
        for (int i =0; i < 3; i += 1) {
            motorInput[i] = motorInput[i]/max;
        }
    }
    for (int i =0; i < 3; i += 1) {
        // scale the motor input to the closed loop multiplier
        motorInput[i] *= TALON_CLOSED_LOOP_MULTIPLIER;
        motors[i]->Set(motorInput[i]);
    }
    SmartDashboard::PutNumber("Motor A: ", motorInput[0]);
    SmartDashboard::PutNumber("Motor B: ", motorInput[1]);
    SmartDashboard::PutNumber("Motor C: ", motorInput[2]);
    SmartDashboard::PutNumber("vX: ", vX);
    SmartDashboard::PutNumber("vY: ", vY);
    SmartDashboard::PutNumber("vZ: ", vZ);
    SmartDashboard::PutNumber("vPID: ", vPID);
    PutDashboard();
}

void Chassis::PutDashboard() {
    SmartDashboard::PutBoolean("Field Oriented: ", fieldOriented);
    SmartDashboard::PutBoolean("PID Enabled: ", gyro_pid->IsEnabled());
    SmartDashboard::PutBoolean("PIDInControl: ", pidInControl);
    SmartDashboard::PutNumber("Set Point: ", lib4774::r2d(gyro_pid->GetSetpoint()));
    double chassis_encoders[4] = {};
    EncoderDistance(chassis_encoders);
    SmartDashboard::PutNumber("Encoder Motor A: ", chassis_encoders[0]);
    SmartDashboard::PutNumber("Encoder Motor B: ", chassis_encoders[1]);
    SmartDashboard::PutNumber("Encoder Motor C: ", chassis_encoders[2]);
    // here we divide by the closed loop multiplier to scale to +- 1
    SmartDashboard::PutNumber("Vel Motor A: ", motor_a->GetSpeed()/TALON_CLOSED_LOOP_MULTIPLIER);
    SmartDashboard::PutNumber("Vel Motor B: ", motor_b->GetSpeed()/TALON_CLOSED_LOOP_MULTIPLIER);
    SmartDashboard::PutNumber("Vel Motor C: ", motor_c->GetSpeed()/TALON_CLOSED_LOOP_MULTIPLIER);
}

void Chassis::ToggleFieldOrient() {
    fieldOriented = !fieldOriented;
    SmartDashboard::PutBoolean("Field Oriented: ", fieldOriented);
}

void Chassis::EnablePID() {
    gyro_pid->Enable();
    SmartDashboard::PutBoolean("PID Enabled: ", gyro_pid->IsEnabled());
}

void Chassis::DisablePID() {
    gyro_pid->Disable();
    SmartDashboard::PutBoolean("PID Enabled: ", gyro_pid->IsEnabled());
}

bool Chassis::OnTarget() {
    return gyro_pid->OnTarget();
}

bool Chassis::PIDEnabled() {
    return gyro_pid->IsEnabled();
}

void Chassis::SetHeading(double newHeading) {
    double newHead = atan2(sin(newHeading),cos(newHeading)); //wrap to +- PI
    gyro_pid->Reset();
    gyro_pid->SetSetpoint(newHead);
    gyro_pid->Enable();
    SmartDashboard::PutNumber("Set Point: ", lib4774::r2d(gyro_pid->GetSetpoint()));
}

void Chassis::HeadingChange(double change) {
    gyro_pid->Reset();
    double newHead = CommandBase::imu->GetYaw()+change;
    newHead = atan2(sin(newHead),cos(newHead)); //wrap to +- PI
    gyro_pid->SetSetpoint(newHead);
    gyro_pid->Enable();
    SmartDashboard::PutNumber("Set Point: ", lib4774::r2d(gyro_pid->GetSetpoint()));
}

void Chassis::EncoderDistance(double* encoder_distance) {
    //motors a b d and e
    encoder_distance[0] = (motor_a->GetPosition()/ENCODER_COUNTS_PER_REVOLUTION)*WHEEL_CIRCUMFERENCE;
    encoder_distance[1] = (motor_b->GetPosition()/ENCODER_COUNTS_PER_REVOLUTION)*WHEEL_CIRCUMFERENCE;
    encoder_distance[2] = -(motor_c->GetPosition()/ENCODER_COUNTS_PER_REVOLUTION)*WHEEL_CIRCUMFERENCE;
}

void Chassis::ZeroEncoders() {
    motor_a->SetPosition(0.0);
    motor_b->SetPosition(0.0);
    motor_c->SetPosition(0.0);
}


