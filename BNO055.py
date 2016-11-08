
from Adafruit_I2C import Adafruit_I2C
import math, sys
import logging

class bno055:

    def __init__(self, addr=None, busnum=0):
        if not addr:
            addr = self.BNO055_ADDRESS_A
        self.addr = addr
        self.i2c = Adafruit_I2C(addr, busnum=busnum)
        self.logger = logging.getLogger("BNO055")

        # set the units and the operation modes of the gyro
        try:
            # read the current units, then flip the appropriate bits
            # units that we set are all are or based off radians
            current_units = self.i2c.readU8(self.BNO055_UNIT_SEL_ADDR)
            self.logger.info("Found device")
            for unit_list in self.BNO055_UNIT_SEL_LIST:
                if unit_list[0] == 1:
                    current_units = current_units | (1 << unit_list[1])
                elif unit_list[0] == 0:
                    current_units = current_units & ~(1 << unit_list[1])
            self.i2c.write8(self.BNO055_UNIT_SEL_ADDR, current_units)
            self.logger.info("Set units")
            # set the operation mode
            self.i2c.write8(self.BNO055_OPR_MODE_ADDR, self.OPERATION_MODE_IMUPLUS)
            self.logger.info("Set op mode")
            # reverse any axis that we may want to
            self.reverse_axis(False, False, False)
            self.logger.info("Reversed axes")
        except:
            self.logger.error("Error setting units for BNO055 device")
        self.offset = 0.0

    def reverse_axis(self, x, y, z):
        """Reverse the axis directions, xyz are booleans"""
        current_directions = self.i2c.readU8(self.BNO055_AXIS_MAP_SIGN_ADDR)
        if x:
            current_directions = current_directions | (1 << 2)
        else:
            current_directions = current_directions & ~ (1 << 2)
        if y:
            current_directions = current_directions | (1 << 1)
        else:
            current_directions = current_directions & ~ (1 << 1)
        if z:
            current_directions = current_directions | (1 << 0)
        else:
            current_directions = current_directions & ~ (1 << 0)
        try:
            self.i2c.write8(self.BNO055_AXIS_MAP_SIGN_ADDR, current_directions)
        except:
            pass

    def reset_heading(self, heading=0.0):
        self.offset = self.get_raw_heading() - heading
        self.logger.info("BNO055: offset reset")

    def get_euler(self, start_register):
        try:
            euler_bytes = [self.i2c.readU8(start_register), self.i2c.readU8(start_register+1)]
            euler_unsigned = euler_bytes[1] << 8 | euler_bytes[0]
            if euler_unsigned > 32767:
                euler_unsigned -= 65536
            euler_signed = float(euler_unsigned) / 900.0
            return euler_signed
        except:
            self.logger.error("Error reading euler angle at register %s" % (start_register))
            return 0.0

    def get_angles(self):
        """ Return the [heading, pitch, roll] of the gyro """
        return [self.get_heading(), self.get_pitch(), self.get_roll()]

    def get_heading(self):
        angle = (self.get_raw_heading() - self.offset)
        return math.atan2(math.sin(angle), math.cos(angle))

    def get_yaw(self):
        return self.get_heading()

    def get_raw_heading(self):
        return -self.get_euler(self.BNO055_EULER_H_LSB_ADDR)

    def get_pitch(self):
        return self.get_euler(self.BNO055_EULER_P_LSB_ADDR)

    def get_roll(self):
        return self.get_euler(self.BNO055_EULER_R_LSB_ADDR)

    def get_heading_rate(self):
        return -self.get_euler(self.BNO055_GYRO_DATA_Z_LSB_ADDR)


    """ I2C addresses, register addresses, and
    values to set registers to for the BNO055"""
    # i2c addresses for the gyro
    # a is when the com3 in input is low
    # b is when it is high
    BNO055_ADDRESS_A = 0X28
    BNO055_ADDRESS_B = 0X29

    BNO055_PAGE_ID_ADDR = 0X07

    BNO055_CHIP_ID_ADDR = 0X00
    BNO055_ACCEL_REV_ID_ADDR = 0X01
    BNO055_MAG_REV_ID_ADDR = 0X02
    BNO055_GYRO_REV_ID_ADDR = 0X03
    BNO055_SW_REV_ID_LSB_ADDR = 0X04
    BNO055_SW_REV_ID_MSB_ADDR = 0X05
    BNO055_BL_REV_ID_ADDR = 0X06

    BNO055_ACCEL_DATA_X_LSB_ADDR = 0X08
    BNO055_ACCEL_DATA_X_MSB_ADDR = 0X09
    BNO055_ACCEL_DATA_Y_LSB_ADDR = 0X0A
    BNO055_ACCEL_DATA_Y_MSB_ADDR = 0X0B
    BNO055_ACCEL_DATA_Z_LSB_ADDR = 0X0C
    BNO055_ACCEL_DATA_Z_MSB_ADDR = 0X0D

    BNO055_MAG_DATA_X_LSB_ADDR = 0X0E
    BNO055_MAG_DATA_X_MSB_ADDR = 0X0F
    BNO055_MAG_DATA_Y_LSB_ADDR = 0X10
    BNO055_MAG_DATA_Y_MSB_ADDR = 0X11
    BNO055_MAG_DATA_Z_LSB_ADDR = 0X12
    BNO055_MAG_DATA_Z_MSB_ADDR = 0X13

    BNO055_GYRO_DATA_X_LSB_ADDR = 0X14
    BNO055_GYRO_DATA_X_MSB_ADDR = 0X15
    BNO055_GYRO_DATA_Y_LSB_ADDR = 0X16
    BNO055_GYRO_DATA_Y_MSB_ADDR = 0X17
    BNO055_GYRO_DATA_Z_LSB_ADDR = 0X18
    BNO055_GYRO_DATA_Z_MSB_ADDR = 0X19

    BNO055_EULER_H_LSB_ADDR = 0X1A  # euler heading, least significant bit
    BNO055_EULER_H_MSB_ADDR = 0X1B  # euler heading, most significant bit
    BNO055_EULER_P_LSB_ADDR = 0X1C  # euler pitch, least significant bit
    BNO055_EULER_P_MSB_ADDR = 0X1D  # euler pitch, most significant bit
    BNO055_EULER_R_LSB_ADDR = 0X1E  # euler roll, least significant bit
    BNO055_EULER_R_MSB_ADDR = 0X1F  # euler roll, most significant bit

    BNO055_QUATERNION_DATA_W_LSB_ADDR = 0X20
    BNO055_QUATERNION_DATA_W_MSB_ADDR = 0X21
    BNO055_QUATERNION_DATA_X_LSB_ADDR = 0X22
    BNO055_QUATERNION_DATA_X_MSB_ADDR = 0X23
    BNO055_QUATERNION_DATA_Y_LSB_ADDR = 0X24
    BNO055_QUATERNION_DATA_Y_MSB_ADDR = 0X25
    BNO055_QUATERNION_DATA_Z_LSB_ADDR = 0X26
    BNO055_QUATERNION_DATA_Z_MSB_ADDR = 0X27

    BNO055_LINEAR_ACCEL_DATA_X_LSB_ADDR = 0X28
    BNO055_LINEAR_ACCEL_DATA_X_MSB_ADDR = 0X29
    BNO055_LINEAR_ACCEL_DATA_Y_LSB_ADDR = 0X2A
    BNO055_LINEAR_ACCEL_DATA_Y_MSB_ADDR = 0X2B
    BNO055_LINEAR_ACCEL_DATA_Z_LSB_ADDR = 0X2C
    BNO055_LINEAR_ACCEL_DATA_Z_MSB_ADDR = 0X2D

    BNO055_GRAVITY_DATA_X_LSB_ADDR = 0X2E
    BNO055_GRAVITY_DATA_X_MSB_ADDR = 0X2F
    BNO055_GRAVITY_DATA_Y_LSB_ADDR = 0X30
    BNO055_GRAVITY_DATA_Y_MSB_ADDR = 0X31
    BNO055_GRAVITY_DATA_Z_LSB_ADDR = 0X32
    BNO055_GRAVITY_DATA_Z_MSB_ADDR = 0X33

    BNO055_TEMP_ADDR = 0X34

    BNO055_CALIB_STAT_ADDR = 0X35
    BNO055_SELFTEST_RESULT_ADDR = 0X36
    BNO055_INTR_STAT_ADDR = 0X37

    BNO055_SYS_CLK_STAT_ADDR = 0X38
    BNO055_SYS_STAT_ADDR = 0X39
    BNO055_SYS_ERR_ADDR = 0X3A

    BNO055_UNIT_SEL_ADDR = 0X3B  # address used to select the unit outputs
    # the units that we want and the index in the unit select register that corrosponds to it
    BNO055_UNIT_SEL_ACC_UNIT = 0  # m/s
    BNO055_UNIT_SEL_ACC_UNIT_INDEX = 0
    BNO055_UNIT_SEL_GYR_UNIT = 1  # rad/s
    BNO055_UNIT_SEL_GYR_UNIT_INDEX = 1
    BNO055_UNIT_SEL_EUL_UNIT = 1  # rad
    BNO055_UNIT_SEL_EUL_UNIT_INDEX = 2
    BNO055_UNIT_SEL_TEMP_UNIT = 0  # celcius
    BNO055_UNIT_SEL_TEMP_UNIT_INDEX = 4
    BNO055_UNIT_SEL_ORI_UNIT = 1  # android orientation mode, pitch turning clockwise decreases values
    BNO055_UNIT_SEL_ORI_UNIT_INDEX = 7
    BNO055_UNIT_SEL_LIST = [[BNO055_UNIT_SEL_ACC_UNIT, BNO055_UNIT_SEL_ACC_UNIT_INDEX],
                [BNO055_UNIT_SEL_GYR_UNIT, BNO055_UNIT_SEL_GYR_UNIT_INDEX],
                [BNO055_UNIT_SEL_EUL_UNIT, BNO055_UNIT_SEL_EUL_UNIT_INDEX],
                [BNO055_UNIT_SEL_TEMP_UNIT, BNO055_UNIT_SEL_TEMP_UNIT_INDEX],
                [BNO055_UNIT_SEL_ORI_UNIT, BNO055_UNIT_SEL_ORI_UNIT_INDEX]]

    BNO055_DATA_SELECT_ADDR = 0X3C

    BNO055_OPR_MODE_ADDR = 0X3D  # the address used to select what sensors to use for the gyro outputs
    # operation modes for the gyro, changes what sensors it uses and how it fuses them
    OPERATION_MODE_CONFIG = 0X00
    OPERATION_MODE_ACCONLY = 0X01
    OPERATION_MODE_MAGONLY = 0X02
    OPERATION_MODE_GYRONLY = 0X03
    OPERATION_MODE_ACCMAG = 0X04
    OPERATION_MODE_ACCGYRO = 0X05
    OPERATION_MODE_MAGGYRO = 0X06
    OPERATION_MODE_AMG = 0X07
    OPERATION_MODE_IMUPLUS = 0X08
    OPERATION_MODE_COMPASS = 0X09
    OPERATION_MODE_M4G = 0X0A
    OPERATION_MODE_NDOF_FMC_OFF = 0X0B
    OPERATION_MODE_NDOF = 0X0C

    BNO055_PWR_MODE_ADDR = 0X3E
    # power modes
    POWER_MODE_NORMAL = 0X00
    POWER_MODE_LOWPOWER = 0X01
    POWER_MODE_SUSPEND = 0X02

    BNO055_SYS_TRIGGER_ADDR = 0X3F
    BNO055_TEMP_SOURCE_ADDR = 0X40

    BNO055_AXIS_MAP_CONFIG_ADDR = 0X41
    # axis map configuration modes
    REMAP_CONFIG_P0 = 0X21
    REMAP_CONFIG_P1 = 0X22
    REMAP_CONFIG_P2 = 0X23
    REMAP_CONFIG_P3 = 0X24
    REMAP_CONFIG_P4 = 0X25
    REMAP_CONFIG_P5 = 0X26
    REMAP_CONFIG_P6 = 0X27
    REMAP_CONFIG_P7 = 0X28
    BNO055_AXIS_MAP_SIGN_ADDR = 0X42
    REMAP_SIGN_P0 = 0X04
    REMAP_SIGN_P1 = 0X00
    REMAP_SIGN_P2 = 0X06
    REMAP_SIGN_P3 = 0X02
    REMAP_SIGN_P4 = 0X03
    REMAP_SIGN_P5 = 0X01
    REMAP_SIGN_P6 = 0X07
    REMAP_SIGN_P7 = 0X05

    BNO055_SIC_MATRIX_0_LSB_ADDR = 0X43
    BNO055_SIC_MATRIX_0_MSB_ADDR = 0X44
    BNO055_SIC_MATRIX_1_LSB_ADDR = 0X45
    BNO055_SIC_MATRIX_1_MSB_ADDR = 0X46
    BNO055_SIC_MATRIX_2_LSB_ADDR = 0X47
    BNO055_SIC_MATRIX_2_MSB_ADDR = 0X48
    BNO055_SIC_MATRIX_3_LSB_ADDR = 0X49
    BNO055_SIC_MATRIX_3_MSB_ADDR = 0X4A
    BNO055_SIC_MATRIX_4_LSB_ADDR = 0X4B
    BNO055_SIC_MATRIX_4_MSB_ADDR = 0X4C
    BNO055_SIC_MATRIX_5_LSB_ADDR = 0X4D
    BNO055_SIC_MATRIX_5_MSB_ADDR = 0X4E
    BNO055_SIC_MATRIX_6_LSB_ADDR = 0X4F
    BNO055_SIC_MATRIX_6_MSB_ADDR = 0X50
    BNO055_SIC_MATRIX_7_LSB_ADDR = 0X51
    BNO055_SIC_MATRIX_7_MSB_ADDR = 0X52
    BNO055_SIC_MATRIX_8_LSB_ADDR = 0X53
    BNO055_SIC_MATRIX_8_MSB_ADDR = 0X54

    ACCEL_OFFSET_X_LSB_ADDR = 0X55
    ACCEL_OFFSET_X_MSB_ADDR = 0X56
    ACCEL_OFFSET_Y_LSB_ADDR = 0X57
    ACCEL_OFFSET_Y_MSB_ADDR = 0X58
    ACCEL_OFFSET_Z_LSB_ADDR = 0X59
    ACCEL_OFFSET_Z_MSB_ADDR = 0X5A

    MAG_OFFSET_X_LSB_ADDR = 0X5B
    MAG_OFFSET_X_MSB_ADDR = 0X5C
    MAG_OFFSET_Y_LSB_ADDR = 0X5D
    MAG_OFFSET_Y_MSB_ADDR = 0X5E
    MAG_OFFSET_Z_LSB_ADDR = 0X5F
    MAG_OFFSET_Z_MSB_ADDR = 0X60

    GYRO_OFFSET_X_LSB_ADDR = 0X61
    GYRO_OFFSET_X_MSB_ADDR = 0X62
    GYRO_OFFSET_Y_LSB_ADDR = 0X63
    GYRO_OFFSET_Y_MSB_ADDR = 0X64
    GYRO_OFFSET_Z_LSB_ADDR = 0X65
    GYRO_OFFSET_Z_MSB_ADDR = 0X66

    ACCEL_RADIUS_LSB_ADDR = 0X67
    ACCEL_RADIUS_MSB_ADDR = 0X68
    MAG_RADIUS_LSB_ADDR = 0X69
    MAG_RADIUS_MSB_ADDR = 0X6A
