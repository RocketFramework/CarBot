import sys
import time
from enum import Enum
from adafruit_servokit import ServoKit
from typing import List

class ServoIds(Enum):
    Looker = 0
    Driver = 1
    
class PcaServo():
    def __init__(self, kit: ServoKit, ServoId: ServoIds, max_angle, min_angle, original_angle, actuation_range) -> None:
        self.kit = kit  # Store the ServoKit instance
        self.MAX_ANGLE = max_angle
        self.MIN_ANGLE = min_angle
        self.channel = ServoId 
        self.angle = original_angle       
        self.actuation_range = actuation_range 
        self.servo_id = ServoId
        
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
            PcaServo(self.kit, ServoIds.Looker, 120, 20, 70, 150),
            PcaServo(self.kit, ServoIds.Driver, 51, 0, 30, 150)
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
