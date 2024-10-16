import keyboard
import math
import time
from typing import List
from .classes.car_engine import CarEngine
from .classes.car_driver import CarFront, CarRear
from .classes.car_eye import CarEye
from .classes.class_config import DRIVER_DEFAULT_ANGLE, DRIVER_MAX_ANGLE, DRIVER_MIN_ANGLE
from .car_config import  MINIMUM_GAP, WHEEL_RADIUS, ONE_WHEEL_TURN_LENGTH, ONE_WHEEL_TURN_STEPS
from .classes.class_config import EYE_MAX_ANGLE

class FullSelfDriving:
    def __init__(self):
        self.carEngine = CarEngine()
        self.carFront = CarFront()
        self.carRear = CarRear()
        self.carEye = CarEye()
        
        self.running = True
        
        keyboard.on_press_key('e', self.stop_loop)
        
    def stop_loop(self, event):
        self.running = False
    
    def handle_cant_move_scenario(self):
        """Eye Max is Left From top of car view
            Driver Max Is Right"""
            
        # Get distance around car
        first_distances = self.carEye.get_distance_around_car()
        # Get rear distance to obstacle
        # Slowly move the car Reverse
        self.carEngine.move_reverse(20)
        # While reversing get the distance around
        while True:
            second_distance = self.carEye.get_distance_around_car()
            if second_distance[0] > first_distances[0]:
                self.carEngine.stop()
                driver_moving_angle = DRIVER_MIN_ANGLE
                break
            
            elif second_distance[1] > first_distances[1]:
                self.carEngine.stop()
                driver_moving_angle = DRIVER_MAX_ANGLE
                break
            
            time.sleep(0.5)
        return driver_moving_angle
    
        # If one side is more than the last saving then go to that direction(greater one)
        # Else If directions are equal, choose right

    def drive(self):

        # Get the distance to obstacle
        can_move = self.carEye.can_i_keep_moving()
        # while it is true

        while self.running:
            print("running")
            # Move the car forward
            # keep geting the distance to the obstacle
            # can_move = self.carEye.can_i_keep_moving()
            if not can_move:
                print("I cant Move")
                self.carEngine.stop()
                to_move_distance, moving_angle = self.carEye.get_the_direction_to_move()
                if to_move_distance == 0:
                    print("distance = 0")
                    moving_angle = self.handle_cant_move_scenario()
                driver_moving_angle = EYE_MAX_ANGLE - moving_angle
                self.carFront.set_front_angle(driver_moving_angle)
                time.sleep(.2)
                self.carFront.set_front_angle(DRIVER_DEFAULT_ANGLE)
                self.carEngine.move_forward(50)
            else:
                self.carEngine.move_forward(50)
                
            can_move = self.carEye.can_i_keep_moving()
            
        keyboard.unhook_all()
        # if it is false then call get_the_direction_to_move(self)    
        self.carEngine.cleanup()
        # set the driver to the correct angle
    
    def turn(self, target_angle, speed):
        """
        Turns the car by target_angle (degrees), adjusting steering during the turn.
        """
        # Initially turn the steering to the full target angle
        self.steering.set_angle(target_angle)
        
        self.car_speed = speed
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
     
def run():
    self_drive = FullSelfDriving()
    self_drive.drive()
        