#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

# Define GPIO pins for the 28BYJ-48 stepper motor
PINS = [17, 27, 22, 23]
STEP_SLEEP = 0.1  # Delay between steps (adjust for visibility)

# Stepper motor sequence for 28BYJ-48
HALF_STEP_SEQUENCE = [
    [1, 0, 0, 1],
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1]
]

STEP_SEQUENCE = [
    [1, 0, 0, 0],  # Step 1
    [1, 1, 0, 0],  # Step 2
    [0, 1, 0, 0],  # Step 3
    [0, 1, 1, 0],  # Step 4
    [0, 0, 1, 0],  # Step 5
    [0, 0, 1, 1],  # Step 6
    [0, 0, 0, 1],  # Step 7
    [1, 0, 0, 1]   # Step 8
]

# Setup GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(PINS, GPIO.OUT)

# Function to rotate the motor
def rotate_motor(steps, direction):
    motor_step_counter = 0
    for _ in range(steps):
        for pin in range(4):
            GPIO.output(PINS[pin], STEP_SEQUENCE[motor_step_counter][pin])
        
        motor_step_counter = (motor_step_counter + (1 if direction else -1)) % len(STEP_SEQUENCE)
        time.sleep(STEP_SLEEP)

# Main execution
try:
# """     print("Rotating clockwise...")
#     rotate_motor(512, True)  # Rotate 512 steps clockwise
#     time.sleep(1)  # Wait for a moment """

    print("Rotating counter-clockwise...")
    rotate_motor(4096, False)  # Rotate 512 steps counter-clockwise

except KeyboardInterrupt:
    print("Stopped by user")
finally:
    GPIO.cleanup()
