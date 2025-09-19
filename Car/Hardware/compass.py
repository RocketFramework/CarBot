from smbus2 import SMBus   # import SMBus module of I2C
from time import sleep     # import sleep
from Car.config import COMPASS_SMOOTHING_FACTOR
import math

class Gy273:
    def __init__(self, bus_number=3, device_address=0x1e):
        self.bus = SMBus(bus_number)  # Use I²C bus 1 (default on Pi 4)
        self.device_address = device_address  # HMC5883L magnetometer address
        self.pi = 22/7  # approximate pi
        self.magnetometer()
        self.smoothed_heading = None
        self.raw_heading = 0
        self.smoothed_heading = None

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
        if value > 32767:
            value -= 65536
        return value

    def get_raw_angle(self):
        while True:
            x = self.read_raw_data(0x03)  # X-axis MSB data register
            z = self.read_raw_data(0x05)  # Z-axis MSB data register
            y = self.read_raw_data(0x07)  # Y-axis MSB data register

            heading = math.atan2(y, x)   # just raw atan2

            if heading < 0:
                heading += 2 * self.pi
            if heading > 2 * self.pi:
                heading -= 2 * self.pi
            
            return int(heading * 180 / self.pi)  # Convert to degrees
        time.sleep(.1)
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

    def get_heading_angle(self):
        while True:
            self.raw_heading = self.get_raw_angle()
            if self.smoothed_heading is None:
                self.smoothed_heading = self.raw_heading
            else:
                self.smoothed_heading = (COMPASS_SMOOTHING_FACTOR * self.raw_heading) + ((1 - COMPASS_SMOOTHING_FACTOR) * self.smoothed_heading)
            sleep(.1)   
            return int(self.smoothed_heading)


def run():
    gy273 = Gy273() 
    print("Reading Heading Angle")

    while True:
        gy273.raw_heading = gy273.get_heading_angle()
        if gy273.smoothed_heading is None:
            gy273.smoothed_heading = gy273.raw_heading
        else:
            gy273.smoothed_heading = (COMPASS_SMOOTHING_FACTOR * gy273.raw_heading) + ((1 - COMPASS_SMOOTHING_FACTOR) * gy273.smoothed_heading)

        print(f"Heading = {int(gy273.smoothed_heading)}°")
        sleep(0.1)
if __name__ == "__main__":
    run()
