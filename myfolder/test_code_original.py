import time
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)
i =0
kit.servo[i].actuation_range = 150

kit.servo[i].angle = 92

# kit.servo[i].angle = 0
