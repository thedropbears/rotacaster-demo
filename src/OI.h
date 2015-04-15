#ifndef OI_H
#define OI_H

#include "WPILib.h"

/* This is the OI class.
 * The purpose of this class is to process
 * inputs from the joystick and either output
 * a number that can be used by commands
 * (e.g. the function to get the joystick's
 * current throttle) and call commands when the
 * driver presses specific buttons on the joystick
 * (through the button classes)
 */

class OI
{
private:
    Joystick* JoyDrv;

    Button* gyroResetButton;
    Button* fieldOrientButton;
    Button* togglePIDButton;
public:
    OI();
    Joystick* getJoyDrv();
    double getJoyDrvX();
    double getJoyDrvY();
    double getJoyDrvZ();
    double getJoyDrvThrottle();
};

#endif
