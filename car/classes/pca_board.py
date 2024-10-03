import sys
import time
from enum import Enum
from .class_config import DRIVER_DEFAULT_ANGLE, DRIVER_ACTUATION_ANGLE, DRIVER_MAX_ANGLE, DRIVER_MIN_ANGLE, EYE_DEFAULT_ANGLE, EYE_ACTUATION_ANGLE,\
    EYE_MAX_ANGLE, EYE_MIN_ANGLE
    
import platform
from unittest.mock import MagicMock

# Detect the platform (Windows or Raspberry Pi)
if platform.system() == "Windows":
    # Mock the ServoKit class for Windows development
    class ServoKit:
        def __init__(self, channels):
            self.channels = channels
            self.servo = MagicMock()

        # Mock method to set angle
        def set_angle(self, channel, angle):
            self.servo[channel].angle = angle
            print(f"Mock: Set servo {channel} to {angle} degrees")

else:
    # Use the actual library on Raspberry Pi
    from adafruit_servokit import ServoKit
    
from typing import List

class ServoIds(Enum):
    Looker = 0
    Driver = 1
    
class PcaServo():
    def __init__(self, kit: ServoKit, ServoId: ServoIds) -> None:
        self.servo_id = ServoId      
        self.kit = kit  # Store the ServoKit instance
        self.channel = ServoId 
        self.kit.servo[ServoId.value].actuation_range
        self.MAX_ANGLE = 0
        self.MIN_ANGLE = 0
        self.angle = 0
        self.actuation_range= 0
        
    @property
    def MIN_ANGLE(self):
        return self.MIN_ANGLE 
      
    @property
    def angle(self):
        return self.angle
        
    @property
    def actuation_range(self):
        return self.actuation_range
            
    @property
    def MAX_ANGLE(self):
        return self.MAX_ANGLE 
            
    @MAX_ANGLE.setter
    def MAX_ANGLE(self, angle):
        self.MAX_ANGLE = angle
       
    @MIN_ANGLE.setter
    def MIN_ANGLE(self, angle):
        self.MIN_ANGLE = angle
        
    def rotate(self, angle: int) -> int:
        # Use self.servo_id to access the correct servo
        if angle > self.MAX_ANGLE: 
            self.kit.servo[self.servo_id.value].angle = self.MAX_ANGLE
        elif angle < self.MIN_ANGLE:
            self.kit.servo[self.servo_id.value].angle = self.MIN_ANGLE
        else:    
            self.kit.servo[self.servo_id.value].angle = angle
        return self.kit.servo[self.servo_id.value].angle
            
class PCABoard():
    def __init__(self): 
        self.kit = ServoKit(channels=16)  # Initialize the ServoKit instance
        
        self._driver_servo = PcaServo(self.kit, ServoIds.Looker)
        self._driver_servo.MAX_ANGLE = DRIVER_MAX_ANGLE
        self._driver_servo.MIN_ANGLE = DRIVER_MIN_ANGLE
        self._driver_servo.angle = DRIVER_DEFAULT_ANGLE    
        self._driver_servo.actuation_range = DRIVER_ACTUATION_ANGLE
        
        self._eye_servo = PcaServo(self.kit, ServoIds.Driver)
        self._eye_servo.MAX_ANGLE = EYE_MAX_ANGLE
        self._eye_servo.MIN_ANGLE = EYE_MIN_ANGLE
        self._eye_servo.angle = EYE_DEFAULT_ANGLE    
        self._eye_servo.actuation_range = EYE_ACTUATION_ANGLE
        
        self.PcaServos = {
            self._driver_servo,
            self._eye_servo
        }    
        
        for pcaServo in self.PcaServos:                   
            pcaServo.rotate(pcaServo.angle)
            time.sleep(.1)  
   
    @property
    def eye_servo(self) -> PcaServo:
        """Getter for the PcaServo property (read-only)."""
        return self._eye_servo
    
    @property
    def driver_servo(self) -> PcaServo:
        """Getter for the PcaServo property (read-only)."""
        return self._driver_servo
    
    def run():
        pass
    
if __name__ == '__main__':
    pcaBoard = PCABoard()
