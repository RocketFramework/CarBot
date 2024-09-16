# Import all Modules
import serial, time
import numpy

# Define the UART Device
Lidar_Sensor_Port = serial.Serial("/dev/serial0", 115200,timeout=0)

# Read the distance to the obstacle
def Get_Distance_To_Obstacle():
    Count = Lidar_Sensor_Port.in_waiting
    if Count > 8:
        Bytes = ser.read(9)
        Lidar_Sensor_Port.reset_input_buffer()
        
        if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59:
            distance = Bytes[2] + Bytes[3]*256
            return distance/100.0
        
if not Lidar_Sensor_Port.isOpen():
    Lidar_Sensor_Port.open()

distance = Get_Distance_To_Obstacle()

Lidar_Sensor_Port.close()