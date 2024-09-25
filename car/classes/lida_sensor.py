# Import all Modules
import time
import numpy
import platform
from .mock_serial import MockSerial
# Real class for Raspberry Pi
try:
    import serial
except ImportError:
    serial = None

#implement a class for lidar sensor
class LidarSensor:
    def __init__(self, port="/dev/serial0", baudrate=115200, timeout=1):
        if platform.system() == "Windows":
            # Use mock serial class in Windows
            self.lidar_port = MockSerial(port, baudrate, timeout)
        else:
            # Use real serial class on Raspberry Pi
            if serial is None:
                raise RuntimeError("serial module is not available on this platform")
            self.lidar_port = serial.Serial(port, baudrate, timeout=timeout)

        if not self.lidar_port.is_open:
            self.lidar_port.open()

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
                    return distance / 100  # Return distance in meters
                time.sleep(0.1)

    def close(self):
        """
        Closes the LIDAR sensor port.
        """
        self.lidar_port.close()
        
if __name__ == "__main__":
    lidar = LidarSensor()
    try:
        while True:
            distance = lidar.get_distance_to_obstacle()
            print(f"Distance To Obstacle : {distance} m")
            time.sleep(1)  # Add a delay between readings
    except KeyboardInterrupt:
        lidar.close()
        print("LIDAR connection closed.")
   