#ifndef ROBOTMAP_H
#define ROBOTMAP_H

#include "WPILib.h"

/**
 * The RobotMap is a mapping from the ports sensors and actuators are wired into
 * to a variable name. This provides flexibility changing wiring, makes checking
 * the wiring easier and significantly reduces the number of magic numbers
 * floating around.
 */

// For example to map the left and right motors, you could define the
// following variables to use with your drivetrain subsystem.
//const int LEFTMOTOR = 1;
//const int RIGHTMOTOR = 2;

// If you are using multiple modules, make sure to define both the port
// number and the module. For example you with a rangefinder:
//const int RANGE_FINDER_PORT = 1;
//const int RANGE_FINDER_MODULE = 1;

/* these are the CAN bus ID mappings for the drive motors
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

#endif
