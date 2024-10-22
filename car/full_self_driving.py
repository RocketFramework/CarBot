#import keyboard
import math
import time
import threading
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
        
        self.running = False
        self.lock = threading.Lock()
        #keyboard.on_press_key('e', self.stop_loop)
        
    def stop_loop(self):
        print("stop CALLED")
        with self.lock:
            self.running = False
        print(f"stop {self.running}")
    
    def cleanup(self):
        self.carEngine.cleanup()
        
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
        try:
            with self.lock:
                self.running = True
            # Get the distance to obstacle
            can_move = self.carEye.can_i_keep_moving()
            # while it is true

            while True:
                with self.lock:
                    if not self.running:
                        break
                #print("running")
                # Move the car forward
                # keep geting the distance to the obstacle
                # can_move = self.carEye.can_i_keep_moving()
                if not can_move:
                    #print("I cant Move")
                    self.carEngine.stop()
                    to_move_distance, angle = self.carEye.get_the_direction_to_move()
                    if to_move_distance == 0:
                        #print("distance = 0")
                        angle = self.handle_cant_move_scenario()
                    self.carEngine.move_forward(50)  
                    self.car_smart_turn(angle)
                else:
                    self.carEngine.move_forward(50)               
                can_move = self.carEye.can_i_keep_moving()
        finally:    
            #keyboard.unhook_all()
            # if it is false then call get_the_direction_to_move(self)    
            self.carEngine.stop()
        
        # set the driver to the correct angle

    def car_smart_turn(self, angle):
        moving_angle = EYE_MAX_ANGLE - angle
        
        thread1 = threading.Thread(target=self.carDriver.set_reset_front_angle, args=(moving_angle,))
        thread2 = threading.Thread(target=self.carEye.set_reset_front_angle, args=(angle,))
        
        thread1.start()
        thread2.start()
        
        thread1.join()
        thread2.join()
            
            
def run():
    
    self_drive = FullSelfDriving()
    self_drive.drive()
    
    time.sleep(5)
    print("about to stop")
    self_drive.stop_loop()

        