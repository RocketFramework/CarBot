import sys
import platform
from pathlib import Path
import math
# Add the full path of 'my_folder' to sys.path
# if platform.system() == "Windows":
#     sys.path.append(str(Path(r"C:\Users\user_\CarBot\car\classes")))
# else:
#     sys.path.append(str(Path("/home/pi/Desktop/CarBot/car/classes")))

MINIMUM_GAP = 0.33
WHEEL_RADIUS = 0.002
ONE_WHEEL_TURN_LENGTH = 2*math.pi*WHEEL_RADIUS
ONE_WHEEL_TURN_STEPS = 26
WEB_SOCKET_SERVER_IP = "192.168.169.130"
WEB_SOCKET_SERVER_PORT = "8080"
# import lida_sensor 
# import mock_serial
# import mock_gpio
# import motor_control
# import motor
# import stepper_motor
# import servo_motor
# import ultrasonic_sensor
# import car_engine
