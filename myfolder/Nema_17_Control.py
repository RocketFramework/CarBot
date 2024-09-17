import RPi.GPIO as GPIO
import time

# GPIO Pin Definitions
DIR_PIN = 11    # Direction Pin
PUL_PIN = 7  # Pulse Pin

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(PUL_PIN, GPIO.OUT)

# Motor Control Variables
step_delay = 0.001  # Delay between steps (adjust for speed)
steps = 2000        # Number of steps to move

# Function to move the motor
def move_motor(steps, direction):
    # Set motor direction
    GPIO.output(DIR_PIN, direction)
    
    # Move the motor step by step
    for step in range(steps):
        GPIO.output(PUL_PIN, GPIO.HIGH)
        time.sleep(step_delay)
        GPIO.output(PUL_PIN, GPIO.LOW)
        time.sleep(step_delay)

try:
    # Example: Move motor clockwise for 2000 steps
    move_motor(steps, GPIO.HIGH)

    # Wait for a second
    time.sleep(1)

    # Example: Move motor counterclockwise for 2000 steps
    move_motor(steps, GPIO.LOW)

finally:
    # Clean up GPIO on exit
    GPIO.cleanup()
