# config.py

# Import necessary modules
import time
import numpy as np
import platform
from Mock import gpio as MockGPIO

try:
    import RPi.GPIO as GPIO
except (ImportError, RuntimeError):
    GPIO = MockGPIO 
import board
import busio
from adafruit_mcp230xx.mcp23017 import MCP23017

# Initialize I2C bus (Navio2 passes SDA/SCL)
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize MCP23017
mcp = MCP23017(i2c)

# Serial communication settings
SERIAL_TIMEOUT = 1
BAUD_RATE = 115200

# ============================
ULTRASONIC_TRIGGER_PIN = 4
ULTRASONIC_ECHO_PIN = 17

EDGE_SENSOR_L_ECHO_PIN = 27
EDGE_SENSOR_R_ECHO_PIN = 22

# Front motors
FRONT_RPWM_PIN = 13
FRONT_LPWM_PIN = 12
FRONT_REN_PIN  = mcp.get_pin(0)
FRONT_LEN_PIN  = mcp.get_pin(1)

# Rear motors
REAR_RPM_PIN = 11
REAR_LPWM_PIN = 10
REAR_REN_PIN = mcp.get_pin(2)
REAR_LEN_PIN = mcp.get_pin(3)


# Stepper motor configuration
STEPPER_DIR_PIN = 11
STEPPER_PULSE_PIN = 7
STEPPER_STEPS = 2000

# Rear servo motor settings
REAR_CHANNEL = 15 

# ============================

# Driver servo motor settings
DRIVER_DEFAULT_ANGLE = 25
DRIVER_MIN_ANGLE = 0
DRIVER_MAX_ANGLE = 50
DRIVER_ACTUATION_RANGE = 170
DRIVER_CHANNEL = 14

TURN_STEP_SIZE = 1  # TODO: Calibrate turn step size

# Eye servo motor settings
EYE_MAX_ANGLE = 117
EYE_MIN_ANGLE = 67
EYE_ACTUATION_RANGE = 170
EYE_CHANNEL = 0
EYE_DEFAULT_ANGLE = 92
EYE_DEFAULT_STEP = 5

# ============================
HIGH_GAP = 2  # High gap threshold for speed monitoring
MID_GAP = 1.2  # Mid gap threshold for speed monitoring

C_MINIMUM_GAP = 0.5  # Minimum gap for center sensor
L_MINIMUM_GAP = 20 # Minimum gap for left sensor (cm)
R_MINIMUM_GAP = 20  # Minimum gap for right sensor (cm)
MINIMUM_DISTANCE_BACK = 20  # Minimum distance to reverse (cm)
MINIMUM_GAP_AVOID_RATE = 2
# ============================

MINIMUM_SPEED = 50  # Minimum speed to maintain
MID_SPEED = 65  # Mid speed threshold
MAX_SPEED = 100  # Maximum speed limit
REVERSE_SPEED = 50  # Speed for reverse operation

# ============================

if platform.system() == "Windows":
    INFO_LOG_FILE_PATH = r'C:\Users\user_\OneDrive\Documents\CarBot\client_log.log'
    ERROR_LOG_FILE_PATH = r'C:\Users\user_\OneDrive\Documents\CarBot\cronlogfile.log'
    SERVER_LOG = r'C:\Users\user_\OneDrive\Documents\CarBot\server_log.log'
else:
    INFO_LOG_FILE_PATH = '/home/pi/Desktop/CarBot/LOG/client_log.log'
    ERROR_LOG_FILE_PATH = '/home/pi/Desktop/CarBot/LOG/cronlogfile.log'
    SERVER_LOG = '/home/pi/Desktop/CarBot/LOG/server_log.log'
    
# ============================

SLEEP_TIME  = 0.15

# ============================

SERVER_IP = '192.168.1.6'
SERVER_PORT = 65432

# ============================

COMPASS_ACCURACY = 20
COMPASS_SMOOTHING_FACTOR = 0.1
MAX_DIFF_TIME = 1