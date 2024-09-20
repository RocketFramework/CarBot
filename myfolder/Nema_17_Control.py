import RPi.GPIO as GPIO
import time

# GPIO pin setup
DIR_PIN = 8  # Direction pin
PUL_PIN = 10  # Pulse pin

# Clean up any existing GPIO state at the start
GPIO.cleanup()

# Function to initialize GPIO
def setup_gpio():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(DIR_PIN, GPIO.OUT)
    GPIO.setup(PUL_PIN, GPIO.OUT)

# Function to clean up GPIO
def cleanup_gpio():
    GPIO.cleanup()

# Function to set the direction
def set_direction(clockwise=True):
    GPIO.output(DIR_PIN, GPIO.HIGH if clockwise else GPIO.LOW)

# Function to step the motor
def step_motor(steps, delay=0.1):
    for _ in range(steps):
        GPIO.output(PUL_PIN, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(PUL_PIN, GPIO.LOW)
        time.sleep(delay)

try:
    setup_gpio()  # Initialize GPIO setup

    while True:
        set_direction(clockwise=True)  # Set direction to clockwise
        step_motor(steps=1000)          # Make 1000 steps
        time.sleep(1)                  # Wait for 1 second

except KeyboardInterrupt:
    print("Program interrupted")

finally:
    cleanup_gpio()  # Clean up GPIO on exit
