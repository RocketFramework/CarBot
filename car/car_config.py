import sys
from pathlib import Path

# Add the full path of 'my_folder' to sys.path
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