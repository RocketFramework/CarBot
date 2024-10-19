import time
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)
i = 15
kit.servo[i].actuation_range = 150

kit.servo[i].angle = 30
time.sleep(1)
kit.servo[i].angle = 40
time.sleep(1)
kit.servo[i].angle = 20
time.sleep(1)
kit.servo[i].angle = 40
time.sleep(1)
kit.servo[i].angle = 20
# kit.servo[i].angle = 0
