#ifndef COMMAND_BASE_H
#define COMMAND_BASE_H

#include <string>
#include "Commands/Command.h"
#include "Subsystems/ExampleSubsystem.h"
#include "OI.h"
#include "WPILib.h"
#include <lib-4774/subsystems/Mpu6050.h>

/**
 * The base for all commands. All atomic commands should subclass CommandBase.
 * CommandBase stores creates and stores each control system. To access a
 * subsystem elsewhere in your code in your code use CommandBase.examplesubsystem
 */
class CommandBase: public Command
{
public:
    CommandBase(char const *name);
    CommandBase();
    static void init();
    // Create a single static instance of all of your subsystems
    static ExampleSubsystem *examplesubsystem;
    static Mpu6050* imu;
    static OI *oi;
};

#endif