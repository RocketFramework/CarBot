import sys
import time
from enum import Enum
from .class_config import DRIVER_DEFAULT_ANGLE, DRIVER_ACTUATION_ANGLE, DRIVER_MAX_ANGLE, DRIVER_MIN_ANGLE, EYE_DEFAULT_ANGLE, EYE_ACTUATION_ANGLE,\
    EYE_MAX_ANGLE, EYE_MIN_ANGLE
    
from adafruit_servokit import ServoKit
from typing import List

class ServoIds(Enum):
    Looker = 0
    Driver = 1
    
class PcaServo():
    def __init__(self, kit: ServoKit, ServoId: ServoIds) -> None:
        
        self.servo_id = ServoId
        if self.servo_id == ServoIds.Driver:
            self.MAX_ANGLE = DRIVER_MAX_ANGLE
            self.MIN_ANGLE = DRIVER_MIN_ANGLE
            self.angle = DRIVER_DEFAULT_ANGLE    
            self.actuation_range = DRIVER_ACTUATION_ANGLE
            
        elif self.servo_id == ServoIds.Looker:
            self.MAX_ANGLE = EYE_MAX_ANGLE
            self.MIN_ANGLE = EYE_MIN_ANGLE
            self.angle = EYE_DEFAULT_ANGLE    
            self.actuation_range = EYE_ACTUATION_ANGLE
            
        self.kit = kit  # Store the ServoKit instance
        self.channel = ServoId 

        
    
        
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
        self.PcaServos = {
            PcaServo(self.kit, ServoIds.Looker),
            PcaServo(self.kit, ServoIds.Driver)
        }    
        
        for pcaServo in self.PcaServos:
            if pcaServo.servo_id == ServoIds.Looker:
                self._eye_servo = pcaServo
            elif pcaServo.servo_id == ServoIds.Driver:
                self._driver_servo = pcaServo
                
            self.kit.servo[pcaServo.servo_id.value].actuation_range = pcaServo.actuation_range        
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
    
if __name__ == '__main__':
    pcaBoard = PCABoard()
