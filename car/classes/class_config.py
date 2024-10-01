# config.py

# Import necessary modules
import time
import numpy as np
from .mock_gpio import MockGPIO

# Handle GPIO import based on the environment
try:
    import RPi.GPIO as GPIO  # Use real GPIO on Raspberry Pi
except (ImportError, RuntimeError):
    GPIO = MockGPIO  # Use mock GPIO for non-Raspberry Pi environments

# Constants or settings
SERIAL_TIMEOUT = 1
BAUD_RATE = 115200
DRIVER_SERVO_CONTROL_PIN = 4
EYE_SERVO_CONTROL_PIN = 12
STEPPER_DIR_PIN = 11    # Direction Pin
STEPPER_PULSE_PIN = 7  # Pulse Pin
STEPPER_STEPS = 2000
TURN_ANGLE = 15
EYE_DEFAULT_ANGLE = 90

DRIVER_DEFAULT_ANGLE = 25.5
DRIVER_MIN_ANGLE = 0
DRIVER_MAX_ANGLE = 51
DRIVER_ACTUATION_ANGLE = 150

EYE_MAX_ANGLE = 180
EYE_MIN_ANGLE = 0
EYE_ACTUATION_ANGLE = 150 # This must be adjusted

# Utility functions (example)
def delay(seconds):
    time.sleep(seconds)

# Export the specific things you want to expose (optional)
__all__ = ['GPIO', 'time', 'np', 'SERIAL_TIMEOUT', 'BAUD_RATE', 'STEPPER_DIR_PIN', 'STEPPER_PULSE_PIN', 'EYE_SERVO_CONTROL_PIN', 'STEPPER_STEPS', 'delay']
