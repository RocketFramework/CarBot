import RPi.GPIO as GPIO
import time

# Define GPIO pins connected to ULN2003
IN1 = 17
IN2 = 27
IN3 = 22
IN4 = 23

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

# Define the sequence of steps for the motor to rotate
step_sequence = [
    [1, 0, 0, 1],
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1]
]

# Step motor forward
def step_motor(direction, steps, delay):
    for _ in range(steps):
        for step in step_sequence[::direction]:
            GPIO.output(IN1, step[0])
            GPIO.output(IN2, step[1])
            GPIO.output(IN3, step[2])
            GPIO.output(IN4, step[3])
            time.sleep(delay)

try:
    # Rotate motor forward
    step_motor(direction=1, steps=100, delay=0.01)  # adjust steps and delay as needed

    # Rotate motor backward
    step_motor(direction=-1, steps=100, delay=0.01)

finally:
    GPIO.cleanup()
