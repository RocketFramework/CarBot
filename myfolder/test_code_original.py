import time
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)
i =14
kit.servo[i].actuation_range = 150

kit.servo[i].angle = 25


# kit.servo[i].angle = 0
