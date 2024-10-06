import time
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)
i =15
kit.servo[i].actuation_range = 150

kit.servo[i].angle = 0
time.sleep(2) 
kit.servo[i].angle = 51
time.sleep(2)
kit.servo[i].angle = 0
time.sleep(2) 
kit.servo[i].angle = 51
# kit.servo[i].angle = 0
