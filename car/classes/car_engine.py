import time
import sys
import os
from .dc_motor import DcMotor

class CarEngine:
    def __init__(self):
        self.dc_motor = DcMotor()
        
    def move_forward(self, speed):
        self.dc_motor.set_motor_forward(speed)
     
    def move_reverse(self, speed):
        self.dc_motor.set_motor_reverse(speed)
      
    def stop(self):
        self.dc_motor.stop_motor()
        
    def cleanup(self):
        """Cleanup GPIO settings when done."""
        self.dc_motor.cleanup()

def run():
    try:
        car = CarEngine()
        direction = car.move_forward(100)
        time.sleep(100)
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    finally:
        car.stop()
        car.cleanup()
# Example usage:
# if __name__ == "__main__":
#     engine = CarEngine(delay=0.001)
    
#     try:
#         # Move forward for 200 steps
#         engine.move_forward(speed = 100)
        
#         # Move in reverse for 200 steps
#         engine.move_reverse(steps=200)
        
#         # Stop the engine
#         engine.stop()
#     finally:
#         # Ensure GPIO cleanup
#         engine.cleanup()
