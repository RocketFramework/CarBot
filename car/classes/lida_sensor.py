# Import all Modules
import serial, time
import numpy

# Define the UART Device

# Read the distance to the obstacle
def get_distance_to_obstacle():
    lidar_sensor_port = serial.Serial("/dev/serial0", 115200,timeout=1)
    if not lidar_sensor_port.isOpen():
        lidar_sensor_port.open()
    while True:
        count = lidar_sensor_port.in_waiting
        if count > 8:
            bytes = lidar_sensor_port.read(9)
            lidar_sensor_port.reset_input_buffer()
        #   print(bytes)
            if bytes[0] == 0x59 and bytes[1] == 0x59:
                distance = bytes[2] + bytes[3]*256
                return distance/100
                time.sleep(0.1)
    lidar_sensor_port.close() 

if __name__ == "__main__":
    while True:
        distance = get_distance_to_obstacle()
        print(f"Distance To Obstacle : {distance} m")
   