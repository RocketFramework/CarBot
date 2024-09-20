import RPi.GPIO as GPIO
import time

# GPIO pin setup
DIR_PIN = 7  # Direction pin
PUL_PIN = 11  # Pulse pin

# Clean up any existing GPIO state at the start
GPIO.cleanup()

# Function to initialize GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(PUL_PIN, GPIO.OUT)