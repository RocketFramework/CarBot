#import keyboard
import math
import time
from typing import List
from .classes.car_engine import CarEngine
from .classes.car_driver import CarDriver
from .classes.car_eye import CarEye
from .classes.pca_board import PCABoard
from .classes.class_config import DRIVER_DEFAULT_ANGLE
from .car_config import  MINIMUM_GAP, WHEEL_RADIUS, ONE_WHEEL_TURN_LENGTH, ONE_WHEEL_TURN_STEPS
from .classes.class_config import EYE_MAX_ANGLE

class FullSelfDriving:
    def __init__(self):
        self.pca_board = PCABoard()
        self.carEngine = CarEngine()
        self.carDriver = CarDriver(self.pca_board)
        self.carEye = CarEye(self.pca_board)
        
        self.running = True
        
        #keyboard.on_press_key('e', self.stop_loop)
        
    def stop_loop(self, event):
        self.running = False
    
    def handle_cant_move_scenario(self):
        """Eye Max is Left From top of car view
        Driver Max Is Right"""
            
        # Get distance around car
        to_move_distance, moving_angle = self.carEye.get_the_direction_to_move()
        if to_move_distance == 0:
            # Get rear distance to obstacle
            # Slowly move the car Reverse
            self.step_reverse(50)
            to_move_distance, moving_angle = self.carEye.get_the_direction_to_move()
            # While reversing get the distance around
            while to_move_distance == 0:
                self.step_reverse(50)
                to_move_distance, moving_angle = self.carEye.get_the_direction_to_move()
            return moving_angle
        else:
            return moving_angle
    
        # If one side is more than the last saving the
    def reverse(self, speed):
        self.carEngine.move_reverse(speed)

    def step_reverse(self, speed):
        self.reverse(speed)
        time.sleep(1)
        self.carEngine.stop()
        
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
                to_move_distance, angle = self.carEye.get_the_direction_to_move()
                if to_move_distance == 0:
                    print("distance = 0")
                    moving_angle = self.handle_cant_move_scenario()
                moving_angle = EYE_MAX_ANGLE - angle
                self.carEngine.move_forward(50)  
                self.carDriver.set_reset_front_angle(moving_angle)
            else:
                self.carEngine.move_forward(50)               
            can_move = self.carEye.can_i_keep_moving()
            
        #keyboard.unhook_all()
        # if it is false then call get_the_direction_to_move(self)    
        self.carEngine.cleanup()
        # set the driver to the correct angle
    
    def turn_and_move(self, target_angle, speed):
        """
        Turns the car by target_angle (degrees), adjusting steering during the turn.
        """
        
        self.carDriver.set_front_angle(target_angle)
        angle_diff = abs(target_angle - DRIVER_DEFAULT_ANGLE)
        # Calculate the duration needed to make the turn
        turn_duration = self.calculate_turn_duration(angle_diff, speed)
        # Gradually correct the steering during the turn
        correction_steps = 10  # Number of steps to gradually return the steering
        correction_interval = turn_duration / correction_steps
        self.carEngine.move_forward(50)
        for step in range(1, correction_steps + 1):
            # Gradually return the steering to 0 degrees
            adjusted_angle = angle_diff * (1 - step / correction_steps)
            if (DRIVER_DEFAULT_ANGLE < target_angle):
                self.carDriver.set_front_angle(target_angle - adjusted_angle)
            else:
                self.carDriver.set_front_angle(target_angle + adjusted_angle)
            # Move forward a bit before adjusting the steering again
            time.sleep(correction_interval)
            
        # Ensure the steering is fully straight after the turn
        self.carDriver.set_front_angle(DRIVER_DEFAULT_ANGLE)
        
    def calculate_turn_duration(self, target_angle, speed):
        """
        Calculates how long it takes to turn the car based on the target angle and speed.
        """
        # Assumed baseline: At speed 1.0, a 90-degree turn takes 2 seconds
        base_time = 100.0  # Time in seconds for a 90-degree turn at speed 1.0
        time_for_angle = (abs(target_angle) / 90) * base_time
        
        # Adjust based on the speed (slower speed -> longer time)
        adjusted_time = time_for_angle / speed
        
        return adjusted_time
     
def run():
    
    self_drive = FullSelfDriving()
    self_drive.carEngine.move_forward(50)
    self_drive.carDriver.set_reset_front_angle(0)
        