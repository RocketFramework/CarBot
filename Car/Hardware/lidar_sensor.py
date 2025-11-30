# Import all Modules

import time
import numpy
import platform
from Mock import serial as MockSerial
from Car.config import SERIAL_TIMEOUT, BAUD_RATE
# Real class for Raspberry Pi
try:
    import serial
except ImportError:
    serial = None

#implement a class for lidar sensor
class TF_Luna:
    def __init__(self, port="/dev/serial0"):
        self.BAUD_RATE = BAUD_RATE
        self.SERIAL_TMEOUT = SERIAL_TIMEOUT
        
        if platform.system() == "Windows":
            # Use mock serial class in Windows
            self.lidar_port = MockSerial(port, self.BAUD_RATE, self.SERIAL_TMEOUT)
        else:
            # Use real serial class on Raspberry Pi
            if serial is None:
                raise RuntimeError("serial module is not available on this platform")
            self.lidar_port = serial.Serial(port, self.BAUD_RATE, timeout= self.SERIAL_TMEOUT)

        if not self.lidar_port.is_open:
            self.lidar_port.open()

    def get_data(self):
        return "I get your call"
    
    def get_distance_to_obstacle(self):
        """
        Reads the distance to the obstacle from the LIDAR sensor and returns it in meters.
        """
        while True:
            count = self.lidar_port.in_waiting
            if count > 8:
                bytes_data = self.lidar_port.read(9)
                self.lidar_port.reset_input_buffer()        
                if bytes_data[0] == 0x59 and bytes_data[1] == 0x59:
                    distance = bytes_data[2] + bytes_data[3] * 256
                    strength = bytes_data[4] + bytes_data[5] * 256
                    if strength < 100:
                        distance = 800
                    print(f"distance to object = {distance} cm, strength = {strength}")
                    return distance / 100  # Return distance in meters

            time.sleep(0.1)  
    
    def close(self):
        """
        Closes the LIDAR sensor port.
        """
        self.lidar_port.close()
        
if __name__ == "__main__":
    lidar = TF_Luna()
    try:
        while True:
            distance = lidar.get_distance_to_obstacle()
            print(f"Distance To Obstacle : {distance} m")
            time.sleep(1)  # Add a delay between readings
    except KeyboardInterrupt:
        lidar.close()
        #print("LIDAR connection closed.")
   
def run():
    lidar = TF_Luna()
    try:
        while True:
            distance = lidar.get_distance_to_obstacle()
            print(f"Distance To Obstacle : {distance} m")
            time.sleep(1)  # Add a delay between readings
    except KeyboardInterrupt:
        lidar.close()
        #print("LIDAR connection closed.")