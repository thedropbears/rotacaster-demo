#ifndef GYROCORRECTION
#define GYROCORRECTION

/* The GyroCorrection subsysem takes the output of
 * the robot's yaw pid loop and translates it into
 * a value that can be sent to the robot's motors
 * to correct it's heading.
 */

#include "WPILib.h"

class GyroCorrection: public PIDOutput
{
private:
public:
    void PIDWrite(float output);
    float correction = 0;
};

#endif
