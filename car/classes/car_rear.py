
from .pca_board import PCABoard

class CarRear:
    
    def __init__(self) -> None:
        self.servo = PCABoard()._rear_servo
        self.current_angle = self.servo.angle
    
    def set_angle(self, angle):
        self.current_angle = self.servo.rotate(angle)
        
    # The subclass will still inherit the turn_left() and turn_right() methods
    def turn_left(self, angle_step=5) -> tuple[bool, int]:
        self.current_angle += angle_step
        temp_angle = self.servo.rotate(self.current_angle)
        is_moved = bool(temp_angle==self.current_angle)
        self.current_angle = temp_angle
        return {is_moved, self.current_angle}
    
    def turn_right(self, angle_step=5) -> tuple[bool, int]:
        self.current_angle -= angle_step
        temp_angle = self.servo.rotate(self.current_angle)
        is_moved = (temp_angle==self.current_angle)
        self.current_angle = temp_angle
        return {is_moved, self.current_angle}
    
