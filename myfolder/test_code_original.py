import time
from adafruit_servokit import ServoKit
import RPi.GPIO as GPIO
#85

kit = ServoKit(channels=16)
i = 0
kit.servo[i].actuation_range = 160

kit.servo[i].angle = 117
