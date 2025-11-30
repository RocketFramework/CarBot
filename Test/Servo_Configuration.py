#!/usr/bin/env python3
import time
from navio2 import pwm

# Channel numbers: 0, 1, 2, 3
servo = pwm.PWM(0)  # Use 0 for first PWM output

# Initialize PWM
servo.initialize()
servo.set_period(20)  # 20 ms period typical for RC servos

try:
    while True:
        print("Moving to 0 degrees")
        servo.set_duty_cycle(5)   # ~0 degrees
        time.sleep(1)

        print("Moving to 90 degrees")
        servo.set_duty_cycle(7.5) # ~90 degrees
        time.sleep(1)

        print("Moving to 180 degrees")
        servo.set_duty_cycle(10)  # ~180 degrees
        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting...")
    servo.disable()
