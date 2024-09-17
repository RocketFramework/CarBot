# Import all Modules
import serial, time
import numpy

# Define the UART Device
Lidar_Sensor_Port = serial.Serial("/dev/serial0", 115200,timeout=1)

# Read the distance to the obstacle
def Get_Distance_To_Obstacle():
    while True:
        Count = Lidar_Sensor_Port.in_waiting
        if Count > 8:
            Bytes = Lidar_Sensor_Port.read(9)
            Lidar_Sensor_Port.reset_input_buffer()
        #   print(Bytes)
            if Bytes[0] == 0x59 and Bytes[1] == 0x59:
                distance = Bytes[2] + Bytes[3]*256
                return distance/100
                time.sleep(0.1)
            
if not Lidar_Sensor_Port.isOpen():
    Lidar_Sensor_Port.open()

while True:
    distance = Get_Distance_To_Obstacle()
    print(f"Distance To Obstacle : {distance} m")

Lidar_Sensor_Port.close()