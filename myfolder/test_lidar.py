import serial

try:
    ser = serial.Serial('/dev/serial0', baudrate=115200, timeout=1)
    print("TF-LUNA is connected.")
    ser.close()
except serial.SerialException:
    print("TF-LUNA is not connected.")
