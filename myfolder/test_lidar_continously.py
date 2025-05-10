import serial
import time

def check_lidar_connection(port="/dev/serial0", timeout=1.0):
    try:
        with serial.Serial(port, 115200, timeout=timeout) as ser:
            ser.flushInput()
            time.sleep(0.1)
            if ser.in_waiting:
                data = ser.read(9)
                if len(data) == 9 and data[0] == 0x59 and data[1] == 0x59:
                    return True  # Valid TF-Luna frame header
    except serial.SerialException:
        return False
    return False

while True:
    connected = check_lidar_connection()
    print("LiDAR Connected" if connected else "LiDAR Not Detected")
    time.sleep(1)  # Check every second
