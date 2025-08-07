from smbus2 import SMBus   # import SMBus module of I2C
from time import sleep  # import sleep
import math

# some MPU6050 Registers and their Address
Register_A     = 0              # Address of Configuration register A
Register_B     = 0x01           # Address of configuration register B
Register_mode  = 0x02           # Address of mode register

X_axis_H    = 0x03              # Address of X-axis MSB data register
Z_axis_H    = 0x05              # Address of Z-axis MSB data register
Y_axis_H    = 0x07              # Address of Y-axis MSB data register
declination = -0.00669          # define declination angle of location where measurement going to be done
pi          = 3.14159265359     # define pi value


def Magnetometer_Init():
        # write to Configuration Register A
        bus.write_byte_data(Device_Address, Register_A, 0x70)

        # Write to Configuration Register B for gain
        bus.write_byte_data(Device_Address, Register_B, 0xa0)

        # Write to mode Register for selecting mode
        bus.write_byte_data(Device_Address, Register_mode, 0)
    
def read_raw_data(addr):
        # Read raw 16-bit value
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)

        # concatenate higher and lower value
        value = ((high << 8) | low)

        # to get signed value from module
        if(value > 32768):
            value = value - 65536
        return value


# Change here: Use bus 3
bus = SMBus(3)     # Use I2C bus 3 as assigned to GPIO pins 5 and 6
Device_Address = 0x1e    # HMC5883L magnetometer device address

Magnetometer_Init()     # initialize HMC5883L magnetometer 

print("Reading Heading Angle")

while True:
        x = read_raw_data(X_axis_H)
        z = read_raw_data(Z_axis_H)
        y = read_raw_data(Y_axis_H)

        heading = math.atan2(y, x) + declination
        
        if(heading > 2*pi):
            heading = heading - 2*pi

        if(heading < 0):
            heading = heading + 2*pi

        heading_angle = int(heading * 180/pi)

        print("Heading Angle = %d°" % heading_angle)
        sleep(1)
