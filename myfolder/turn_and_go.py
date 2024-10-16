import time
from math import radians
from classes.car_driver import CarFront

class RobotCar:
    def __init__(self, motor, steering):
        self.driver = Driver()
        self.steering = steering

    def turn(self, target_angle, speed):
        """
        Turns the car by target_angle (degrees), adjusting steering during the turn.
        """
        # Initially turn the steering to the full target angle
        self.steering.set_angle(target_angle)
        
        # Move forward while turning
        self.motor.forward(speed)
        
        # Calculate the duration needed to make the turn
        turn_duration = self.calculate_turn_duration(target_angle, speed)
        
        # Gradually correct the steering during the turn
        correction_steps = 10  # Number of steps to gradually return the steering
        correction_interval = turn_duration / correction_steps
        
        for step in range(1, correction_steps + 1):
            # Gradually return the steering to 0 degrees
            adjusted_angle = target_angle * (1 - step / correction_steps)
            self.steering.set_angle(adjusted_angle)
            
            # Move forward a bit before adjusting the steering again
            time.sleep(correction_interval)
        
        # Ensure the steering is fully straight after the turn
        self.steering.set_angle(0)

        # Continue moving forward straight (if needed)
        # Optionally, stop after a brief move forward
        # time.sleep(forward_duration)
        # self.motor.stop()

    def calculate_turn_duration(self, target_angle, speed):
        """
        Calculates how long it takes to turn the car based on the target angle and speed.
        """
        # Assumed baseline: At speed 1.0, a 90-degree turn takes 2 seconds
        base_time = 2.0  # Time in seconds for a 90-degree turn at speed 1.0
        time_for_angle = (abs(target_angle) / 90) * base_time
        
        # Adjust based on the speed (slower speed -> longer time)
        adjusted_time = time_for_angle / speed
        
        return adjusted_time

# Initialize motor and steering objects
motor = Motor()
steering = Steering()

# Create the robot car object
car = RobotCar(motor, steering)

# Example: Turn 30 degrees to the left at 50% speed
target_angle = -30  # Negative for left, positive for right
speed = 0.5  # Speed from 0 to 1 (e.g., 50% speed)

# Execute the turn
car.turn(target_angle, speed)
