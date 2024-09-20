import serial,time
import numpy as np

ser = serial.Serial("/dev/serial0", 115200,timeout=1) # mini UART serial device

def read_tfluna_data():
    while True:
        counter = ser.in_waiting # count the number of bytes of the serial port
        if counter > 8:
            bytes_serial = ser.read(9) # read 9 bytes
            ser.reset_input_buffer() # reset buffer
        #   print(bytes_serial)
            if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59: # check first two bytes
                distance = bytes_serial[2] + bytes_serial[3]*256 # distance in next two bytes
                strength = bytes_serial[4] + bytes_serial[5]*256 # signal strength in next two bytes
                temperature = bytes_serial[6] + bytes_serial[7]*256 # temp in next two bytes
                temperature = (temperature/8.0) - 256.0 # temp scaling and offset
                return distance/100.0,strength,temperature
                time.sleep(0.1)

if ser.isOpen() == False:
    ser.open() # open serial port if not open

distance, strength, temperature = read_tfluna_data() 

def Avoid_obstacles_and_move(func):
    while True:
        distance, strength, temperature = func()

        if distance <= 1:
            print("Obstacle detected Turn The Car")

            distance, strength, temperature = func()
            if distance > 1:
                print(
                    f"Moving forward. Distance to obstacle: {distance} m.")
                distance, strength, temperature = func()
        else:
            print(f"Moving forward. Distance to obstacle: {distance} m.")

print(f"Distance = {distance} m, Strength = {strength} / 65535 (16-bit), Chip Temperature = {temperature} C")
Avoid_obstacles_and_move(read_tfluna_data)
 
ser.close() # close serial port