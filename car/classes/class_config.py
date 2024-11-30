# config.py

# Import necessary modules
import time
import numpy as np
from .mock_gpio import MockGPIO

try:
    import RPi.GPIO as GPIO
except (ImportError, RuntimeError):
    GPIO = MockGPIO 

# Serial communication settings
SERIAL_TIMEOUT = 1
BAUD_RATE = 115200

# Stepper motor configuration
STEPPER_DIR_PIN = 11
STEPPER_PULSE_PIN = 7
STEPPER_STEPS = 2000

# Driver servo motor settings
DRIVER_DEFAULT_ANGLE = 25
DRIVER_MIN_ANGLE = 0
DRIVER_MAX_ANGLE = 50
DRIVER_ACTUATION_RANGE = 150
DRIVER_CHANNEL = 14

TURN_STEP_SIZE = 1  # TODO: Calibrate turn step size

# Eye servo motor settings
EYE_MAX_ANGLE = 117
EYE_MIN_ANGLE = 67
EYE_ACTUATION_RANGE = 150
EYE_CHANNEL = 0
EYE_DEFAULT_ANGLE = 92
EYE_DEFAULT_STEP = 10

# Rear servo motor settings
REAR_CHANNEL = 15 

# Delay function
def delay(seconds):
    time.sleep(seconds)

# Exported elements
__all__ = [
    'GPIO', 'time', 'np', 'SERIAL_TIMEOUT', 'BAUD_RATE',
    'delay', 'EYE_MAX_ANGLE', 'EYE_MIN_ANGLE', 'EYE_DEFAULT_ANGLE',
    'EYE_CHANNEL', 'EYE_DEFAULT_STEP', 'DRIVER_MAX_ANGLE', 'DRIVER_MIN_ANGLE',
    'DRIVER_CHANNEL', 'DRIVER_DEFAULT_ANGLE', 'TURN_STEP_SIZE', 'SERIAL_TIMEOUT', 'BAUD_RATE', 'REAR_CHANNEL'
]
