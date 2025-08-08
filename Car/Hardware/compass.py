from smbus2 import SMBus   # import SMBus module of I2C
from time import sleep  # import sleep
import math

class Gy273:
    def __init__(self, bus_number=3, device_address=0x1e):
        self.bus = SMBus(bus_number)  # Use specified I2C bus
        self.device_address = device_address  # HMC5883L magnetometer device address
        self.declination = -0.00669  # define declination angle of location where measurement going to be done
        self.pi = 3.14159265359  # define pi value
        self.magnetometer()

    def magnetometer(self):
        # write to Configuration Register A
        self.bus.write_byte_data(self.device_address, 0, 0x70)
        # Write to Configuration Register B for gain
        self.bus.write_byte_data(self.device_address, 0x01, 0xa0)
        # Write to mode Register for selecting mode
        self.bus.write_byte_data(self.device_address, 0x02, 0)

    def read_raw_data(self, addr):
        # Read raw 16-bit value
        high = self.bus.read_byte_data(self.device_address, addr)
        low = self.bus.read_byte_data(self.device_address, addr + 1)
        value = ((high << 8) | low)
        if value > 32768:
            value -= 65536
        return value

    def get_heading_angle(self):
        x = self.read_raw_data(0x03)  # X-axis MSB data register
        z = self.read_raw_data(0x05)  # Z-axis MSB data register
        y = self.read_raw_data(0x07)  # Y-axis MSB data register

        heading = math.atan2(y, x) + self.declination
        
        if heading > 2 * self.pi:
            heading -= 2 * self.pi

        if heading < 0:
            heading += 2 * self.pi

        return int(heading * 180 / self.pi)  # Convert to degrees

    def get_heading_direction(self, angle):
        if (angle >= 337.5 or angle < 22.5):
            return "North"
        elif 22.5 <= angle < 67.5:
            return "Northeast"
        elif 67.5 <= angle < 112.5:
            return "East"
        elif 112.5 <= angle < 157.5:
            return "Southeast"
        elif 157.5 <= angle < 202.5:
            return "South"
        elif 202.5 <= angle < 247.5:
            return "Southwest"
        elif 247.5 <= angle < 292.5:
            return "West"
        elif 292.5 <= angle < 337.5:
            return "Northwest"
        
def run():
    gy273 = Gy273()  # Initialize the Gy273 class
    print("Reading Heading Angle")
    
    while True:
        heading_angle = gy273.get_heading_angle()
        print(f"Heading Angle = {heading_angle}°, Direction = {gy273.get_heading_direction(heading_angle)}")
        sleep(1)

if __name__ == "__main__":
    run()  # Run the main function to start reading heading angles