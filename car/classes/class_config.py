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
SERVO_CONTROL_PIN = 4
STEPPER_DIR_PIN = 11    # Direction Pin
STEPPER_PULSE_PIN = 7  # Pulse Pin
STEPPER_STEPS = 2000

# Utility functions (example)
def delay(seconds):
    time.sleep(seconds)

# Export the specific things you want to expose (optional)
__all__ = ['GPIO', 'time', 'np', 'SERIAL_TIMEOUT', 'BAUD_RATE', 'STEPPER_DIR_PIN', 'STEPPER_PULSE_PIN', 'SERVO_CONTROL_PIN', 'STEPPER_STEPS', 'delay']
