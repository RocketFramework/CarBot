import time
import sys
import os
# Now you can import classes
from .lida_sensor import LidarSensor
from .stepper_motor import Stepper_Motor
from .stepper_motor import Direction

class CarEngine:
    def __init__(self, delay=0.001):
        self.stepper_engine = Stepper_Motor()

    def move_forward(self, steps=100):
        """Move the motor forward by a specified number of steps."""
        self.stepper_engine.step(steps, Direction.FORWARD.value)
        self.stepper_engine.stop()

    def move_reverse(self, steps=100):
        """Move the motor in reverse by a specified number of steps."""
        self.stepper_engine.step(steps, Direction.REVERSE.value)
        self.stepper_engine.stop()

    def cleanup(self):
        """Cleanup GPIO settings when done."""
        self.stepper_engine.cleanup()

# Example usage:
if __name__ == "__main__":
    engine = CarEngine(delay=0.001)
    
    try:
        # Move forward for 200 steps
        engine.move_forward(steps=200)
        
        # Move in reverse for 200 steps
        engine.move_reverse(steps=200)
        
        # Stop the engine
        engine.stop()
    finally:
        # Ensure GPIO cleanup
        engine.cleanup()
