import time
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)
kit.servo[0].actuation_range = 150
kit.servo[2].actuation_range = 150

# kit.servo[0].angle = 150
# time.sleep(5) 
# kit.servo[0].angle = 120
# time.sleep(5) 
# kit.servo[0].angle = 90
# time.sleep(5) 
# kit.servo[0].angle = 60
# time.sleep(5) 
# kit.servo[0].angle = 30
# time.sleep(5) 
# kit.servo[0].angle = 0

kit.servo[0].angle = 51
time.sleep(2) 
kit.servo[0].angle = 0
time.sleep(2) 
kit.servo[2].angle = 51
time.sleep(2) 
kit.servo[2].angle = 0