import smbus2
import time
import sys
from enum import Enum
from typing import List
import platform
import logging
from unittest.mock import MagicMock

# Import config variables (you'll need to adjust these imports based on your actual config)
try:
    from Car.config import DRIVER_DEFAULT_ANGLE, DRIVER_ACTUATION_RANGE, DRIVER_MAX_ANGLE, DRIVER_MIN_ANGLE, DRIVER_CHANNEL, EYE_DEFAULT_ANGLE,\
        EYE_ACTUATION_RANGE, EYE_MAX_ANGLE, EYE_MIN_ANGLE, EYE_CHANNEL, REAR_CHANNEL
except ImportError:
    # Default values if config not found
    DRIVER_DEFAULT_ANGLE = 90
    DRIVER_ACTUATION_RANGE = 180
    DRIVER_MAX_ANGLE = 180
    DRIVER_MIN_ANGLE = 0
    DRIVER_CHANNEL = 0
    
    EYE_DEFAULT_ANGLE = 90
    EYE_ACTUATION_RANGE = 180
    EYE_MAX_ANGLE = 180
    EYE_MIN_ANGLE = 0
    EYE_CHANNEL = 1
    
    REAR_CHANNEL = 2

# --- PCA9685 Configuration ---
BUS = 3
PCA_ADDR = 0x40
FREQ = 50  # 50Hz standard servo

# PCA9685 registers
MODE1 = 0x00
PRESCALE = 0xFE

class ServoIds(Enum):
    Looker = EYE_CHANNEL
    Driver = DRIVER_CHANNEL
    Rear = REAR_CHANNEL

class ServoKit:
    """Mock ServoKit class to maintain same interface"""
    def __init__(self, channels=16):
        self.channels = channels
        self.servo = {}
        for i in range(channels):
            self.servo[i] = MagicMock()
        
        # Initialize PCA9685 hardware
        self._init_pca9685()
    
    def _init_pca9685(self):
        """Initialize PCA9685 hardware"""
        self.bus = smbus2.SMBus(BUS)
        
        # Reset PCA9685
        self._write_reg(MODE1, 0x00)
        time.sleep(0.01)
        
        # Set PWM frequency
        prescale_val = int(25000000.0 / (4096 * FREQ) - 1)
        self._write_reg(MODE1, 0x10)  # sleep
        self._write_reg(PRESCALE, prescale_val)
        self._write_reg(MODE1, 0x00)  # wake
        time.sleep(0.01)
    
    def _write_reg(self, reg, value):
        """Write to PCA9685 register"""
        self.bus.write_byte_data(PCA_ADDR, reg, value)
    
    def _angle_to_pulse(self, angle, actuation_range=180, min_pulse=500, max_pulse=2500):
        """Convert angle to PCA9685 pulse value"""
        # Map angle to pulse width in microseconds
        pulse_us = min_pulse + (angle / actuation_range) * (max_pulse - min_pulse)
        pulse_length = 1000000.0 / FREQ / 4096  # us per bit
        pulse = int(pulse_us / pulse_length)
        return pulse
    
    def _set_servo_pulse(self, channel, pulse):
        """Set servo pulse on specific channel"""
        LED0_ON_L = 0x06 + 4 * channel
        self._write_reg(LED0_ON_L, 0)
        self._write_reg(LED0_ON_L + 1, 0)
        self._write_reg(LED0_ON_L + 2, pulse & 0xFF)
        self._write_reg(LED0_ON_L + 3, (pulse >> 8) & 0xFF)
    
    def set_angle(self, channel, angle, actuation_range=180):
        """Set servo to specific angle"""
        pulse = self._angle_to_pulse(angle, actuation_range)
        self._set_servo_pulse(channel, pulse)

class PcaServo():
    def __init__(self, kit: ServoKit, ServoId: ServoIds, act_range) -> None:
        self.servo_id = ServoId      
        self.kit = kit  # Store the ServoKit instance
        self.channel = ServoId.value
        self.actuation_range = act_range
        self.MAX_ANGLE = 0
        self.MIN_ANGLE = 0
        self.MID_ANGLE = 0
        self.angle = 0
        
        # Configure actuation range
        if hasattr(self.kit.servo[self.channel], 'actuation_range'):
            self.kit.servo[self.channel].actuation_range = act_range
        
    def rotate(self, angle: int) -> int:
        # Use self.servo_id to access the correct servo
        if angle > self.MAX_ANGLE: 
            self.kit.set_angle(self.channel, self.MAX_ANGLE, self.actuation_range)
            self.angle = self.MAX_ANGLE
            print("Left Limit Hit")
        elif angle < self.MIN_ANGLE:
            self.kit.set_angle(self.channel, self.MIN_ANGLE, self.actuation_range)
            self.angle = self.MIN_ANGLE
            print("Right Limit Hit")
        else:    
            self.kit.set_angle(self.channel, angle, self.actuation_range)
            self.angle = angle
        
        time.sleep(.1) 
        return self.angle
    
    def reset(self):
        self.kit.set_angle(self.channel, self.MID_ANGLE, self.actuation_range)
        self.angle = self.MID_ANGLE
        time.sleep(.1) 
                   
class PCA9685(): 

    def __init__(self): 
        self.kit = ServoKit(channels=16)  # Initialize the ServoKit instance
        
        self._driver_servo = PcaServo(self.kit, ServoIds.Driver, DRIVER_ACTUATION_RANGE)
        self._driver_servo.MAX_ANGLE = DRIVER_MAX_ANGLE
        self._driver_servo.MIN_ANGLE = DRIVER_MIN_ANGLE
        self._driver_servo.angle = DRIVER_DEFAULT_ANGLE  
        self._driver_servo.MID_ANGLE = DRIVER_DEFAULT_ANGLE  
        
        self._rear_servo = PcaServo(self.kit, ServoIds.Rear, DRIVER_ACTUATION_RANGE)
        self._rear_servo.MAX_ANGLE = DRIVER_MAX_ANGLE
        self._rear_servo.MIN_ANGLE = DRIVER_MIN_ANGLE
        self._rear_servo.angle = DRIVER_DEFAULT_ANGLE  
        self._rear_servo.MID_ANGLE = DRIVER_DEFAULT_ANGLE 
        
        self._eye_servo = PcaServo(self.kit, ServoIds.Looker, EYE_ACTUATION_RANGE)
        self._eye_servo.MAX_ANGLE = EYE_MAX_ANGLE
        self._eye_servo.MIN_ANGLE = EYE_MIN_ANGLE
        self._eye_servo.angle = EYE_DEFAULT_ANGLE  
        self._eye_servo.MID_ANGLE = EYE_DEFAULT_ANGLE  
        
        self.PcaServos = {
            self._driver_servo,
            self._rear_servo,
            self._eye_servo
        }    
        
        for pcaServo in self.PcaServos:                   
            pcaServo.rotate(pcaServo.angle)
   
    @property
    def eye_servo(self) -> PcaServo:
        """Getter for the PcaServo property (read-only)."""
        return self._eye_servo
    
    @property
    def driver_servo(self) -> PcaServo:
        """Getter for the PcaServo property (read-only)."""
        return self._driver_servo

    @property
    def rear_servo(self) -> PcaServo:
        """Getter for the PcaServo property (read-only)."""
        return self._rear_servo
    
    def reset(self):
        for pcaServo in self.PcaServos:                   
            pcaServo.reset() 
        
if __name__ == '__main__':
    pcaBoard = PCA9685()
    
    # Test example
    print("Testing servo control...")
    while True:
        try:
            angle_input = input("Enter servo angle (0-180) for driver servo (or 'q' to quit): ")
            if angle_input.lower() == 'q':
                break
            angle = int(angle_input)
            pcaBoard.driver_servo.rotate(angle)
            print(f"Driver servo set to {angle}°")
        except ValueError:
            print("Please enter a valid number")
        except KeyboardInterrupt:
            break
    
    pcaBoard.reset()