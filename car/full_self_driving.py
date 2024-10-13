import keyboard
import math
import time
from typing import List
from .classes.car_engine import CarEngine
from .classes.car_driver import CarDriver
from .classes.car_eye import CarEye
from .car_config import  MINIMUM_GAP, WHEEL_RADIUS, ONE_WHEEL_TURN_LENGTH, ONE_WHEEL_TURN_STEPS

class FullSelfDriving:
    def __init__(self):
        self.carEngine = CarEngine()
        self.carDriver = CarDriver()
        self.carEye = CarEye()
        
        self.running = True
        
        keyboard.on_press_key('e', self.stop_loop)
        
    def stop_loop(self, event):
        self.running = False
    
    def drive(self):
        # Get the distance to obstacle
        can_move = self.carEye.can_i_keep_moving()
        # while it is true

        while self.running:
            # Move the car forward
            if can_move == True:    
                self.carEngine.move_forward(50)
            # keep geting the distance to the obstacle
            can_move = self.carEye.can_i_keep_moving()
            if not can_move:
                break
            time.sleep(.1)
            
        keyboard.unhook_all()
        # if it is false then call get_the_direction_to_move(self)    
        self.carEngine.stop()
        self.carEngine.cleanup()
        # set the driver to the correct angle
        
def run():
    self_drive = FullSelfDriving()
    self_drive.drive()
        