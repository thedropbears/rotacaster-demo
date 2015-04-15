#ifndef ROBOTMAP_H
#define ROBOTMAP_H

#include "WPILib.h"

/*
 * The RobotMap is a mapping from the ports sensors and actuators are wired into
 * to a variable name. This provides flexibility changing wiring, makes checking
 * the wiring easier. It also is a place to store software constants in one place
 *  and significantly reduces the number of magic numbers floating around.
 */


/* These are the CAN bus ID mappings for the drive motors
the letters go counter clockwise from the front of holly
  ^
  |

  A
 /  \
B -- C  */
const int DRIVE_MOTOR_A_ID = 1;
const int DRIVE_MOTOR_B_ID = 2;
const int DRIVE_MOTOR_C_ID = 3;

// the max forward velocity as read off of the web configuration interface
const int TALON_CLOSED_LOOP_MULTIPLIER = 472;

// these represent what buttons on the joystick do what (they are used in OI)
const int GYRO_RESET_BUTTON = 11;
const int FIELD_ORIENT_BUTTON = 12;
const int TOGGLE_PID_BUTTON = 10;


// These define the amount the joystick has to be pushed (relative to its max
// push in that axis) where the push is not registered by the code so the
// robot is not constantly moving from the driver's nudges.
const double JOY_DRV_DEAD_X = 0.05;
const double JOY_DRV_DEAD_Y = 0.05;
const double JOY_DRV_DEAD_Z = 0.6;

// These are the amount that each axis is scaled down by at all levels
// (e.g. if the joystick is pushed to 0.5 and the scale is 0.5 the
// output to the chassis' drive function is 0.25)
const double JOYSTICK_X_SCALE = 1.0;
const double JOYSTICK_Y_SCALE = 1.0;
const double JOYSTICK_Z_SCALE = 1.0;

// this is black magic. touch at own risk
const double JOYSTICK_X_EXPONENTIAL = 10;
const double JOYSTICK_Y_EXPONENTIAL = 10;
const double JOYSTICK_Z_EXPONENTIAL = 40;

// the circumference on the wheels of the bot
const double WHEEL_CIRCUMFERENCE = 39.2699081699; //cm
// 7 counts per rev of the motor * for for quad encoder
// * 50 for gear reduction
const double ENCODER_COUNTS_PER_REVOLUTION = 1400;

#endif
