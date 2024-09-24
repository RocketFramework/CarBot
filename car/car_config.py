import sys
import platform
from pathlib import Path

# Add the full path of 'my_folder' to sys.path
if platform.system() == "Windows":
    sys.path.append(str(Path(r"C:\Users\user_\CarBot\car\classes")))
else:
    sys.path.append(str(Path("/home/pi/Desktop/CarBot/car/classes")))

import lida_sensor
import mock_serial
import mock_gpio
import motor_control
import motor
import stepper_motor
import servo_motor
import ultrasonic_sensor
import car_engine