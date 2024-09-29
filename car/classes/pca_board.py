import sys
import time
from adafruit_servokit import ServoKit

class PCABoard():
    def __init__(self, channel, angle, actuation_range):
        self.MAX_ANGLE = 51
        self.MIN_ANGLE = 0
        self.channel = channel 
        self.angle = angle  
        self.actuation_range = actuation_range  
        
        self.kit = ServoKit(channels=16) 
        self.kit.servo[self.channel].actuation_range = self.actuation_range
        
       
        if self.angle > self.MAX_ANGLE or self.angle < self.MIN_ANGLE:
            print("Angle value is too high/low")
            sys.exit()
        else:    
            self.kit.servo[self.channel].angle = self.angle
        
