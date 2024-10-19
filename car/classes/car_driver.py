import time
from .class_config import DRIVER_DEFAULT_ANGLE
from .pca_board import PCABoard

class CarDriver:
    
    def __init__(self, pca_board) -> None:
        
        self.front_servo = pca_board.driver_servo
        self.rear_servo = pca_board.rear_servo
        self.current_front_angle = self.front_servo.angle
        self.current_rear_angle = self.rear_servo.angle
        
    def set_front_angle(self, angle):
        self.current_front_angle = self.front_servo.rotate(angle)
    
    def set_reset_front_angle(self, angle): 
        step = 1
        steps = abs(angle - DRIVER_DEFAULT_ANGLE)// step
        if angle > DRIVER_DEFAULT_ANGLE:
            # Start from Default angle and move until it hit the angle
            for i in range(steps):
                temp_angle = DRIVER_DEFAULT_ANGLE + i
                if temp_angle >= angle:
                    break
                self.set_front_angle(temp_angle)
                time.sleep(.1)
            # Then turn back until it hit the Default angle   
            for i in range(steps):
                temp_angle = angle - i
                if temp_angle <= DRIVER_DEFAULT_ANGLE:
                    break
                self.set_front_angle(temp_angle)
                time.sleep(.1)
        
        else:
            for i in range(steps):
                temp_angle = DRIVER_DEFAULT_ANGLE - i
                if temp_angle <= angle:
                    break
                self.set_front_angle(temp_angle)
                time.sleep(.1)
            
            for i in range(steps):
                temp_angle = angle + i
                if temp_angle >= DRIVER_DEFAULT_ANGLE:
                    break
                self.set_front_angle(temp_angle)
                time.sleep(.1)
            
    # The subclass will still inherit the turn_left() and turn_right() methods
    def front_turn_left(self, angle_step=5) -> tuple[bool, int]:
        self.current_front_angle += angle_step
        temp_angle = self.front_servo.rotate(self.current_front_angle)
        is_moved = bool(temp_angle==self.current_front_angle)
        self.current_front_angle = temp_angle
        return [is_moved, self.current_front_angle]
    
    def front_turn_right(self, angle_step=5) -> tuple[bool, int]:
        self.current_front_angle -= angle_step
        temp_angle = self.front_servo.rotate(self.current_front_angle)
        is_moved = (temp_angle==self.current_front_angle)
        self.current_front_angle = temp_angle
        return [is_moved, self.current_front_angle]
    
    def set_rear_angle(self, angle):
        self.current_rear_angle = self.rear_servo.rotate(angle)
        
    # The subclass will still inherit the turn_left() and turn_right() methods
    def rear_turn_left(self, angle_step=5) -> tuple[bool, int]:
        self.current_rear_angle += angle_step
        temp_angle = self.rear_servo.rotate(self.current_rear_angle)
        is_moved = bool(temp_angle==self.current_rear_angle)
        self.current_rear_angle = temp_angle
        return [is_moved, self.current_rear_angle]
    
    def rear_turn_right(self, angle_step=5) -> tuple[bool, int]:
        self.current_rear_angle -= angle_step
        temp_angle = self.rear_servo.rotate(self.current_rear_angle)
        is_moved = (temp_angle==self.current_rear_angle)
        self.current_rear_angle = temp_angle
        return [is_moved, self.current_rear_angle]   
