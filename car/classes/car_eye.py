import math
import time
from .pca_board import PCABoard
from .lida_sensor import LidarSensor
from car.car_config import MINIMUM_GAP
from .car_engine import CarEngine
# Subclass (CarEye)
class CarEye():
    
    def __init__(self):
        # Custom initialization for CarEye, no call to super().__init__()
        self.servo = PCABoard().eye_servo
        self.lidar_sensor = LidarSensor()
        # self.current_angle = self.servo.angle
    def set_angle(self, angle):
        self.servo.rotate(angle)
        
    # The subclass will still inherit the turn_left() and turn_right() methods
    def turn_left(self, angle_step=10) -> [bool, int]:
        self.servo.angle += angle_step
        temp_angle = math.ceil(self.servo.rotate(self.servo.angle))
        is_moved = (temp_angle==self.servo.angle)
        self.servo.angle = temp_angle
        return [is_moved, self.servo.angle]
    
    def turn_right(self, angle_step=10) -> [bool, int]:
        self.servo.angle -= angle_step
        temp_angle = math.ceil(self.servo.rotate(self.servo.angle))
        is_moved = (temp_angle==self.servo.angle)
        self.servo.angle = temp_angle
        return [is_moved, self.servo.angle]
    
    def get_the_direction_to_move(self) -> [int, float]:
        # reset the servo to its default angle
        self.servo.reset()
        # Create an array to store distances and angles
        input_datas = [(0, 0)]
        # assign the definition to a variable
        turn_data = [True, 0]      
        # Create a while is_moved == True loop
        while turn_data[0] == True:
            # Turn 10 steps right and get distance to the obstacle
            turn_data = self.turn_right()
            if turn_data[0] == True:
                distance = self.lidar_sensor.get_distance_to_obstacle()
                print(f"distance:{distance}, angle: {turn_data[1]}")
                # Store this distance and angle in a array 
                input_datas.append((distance, turn_data[1]))
                # Center the eye servo
            
        self.servo.reset()
        turn_data = [True, 0]    
        while turn_data[0] == True:
            # Turn 10 steps left and get distance to the obstacle
            turn_data = self.turn_left()
            if turn_data[0] == True:
                distance = self.lidar_sensor.get_distance_to_obstacle()
                print(f"distance:{distance}, angle: {turn_data[1]}")
                # Store this distance and angle in a array 
                input_datas.append((distance, turn_data[1]))
                # Center the eye servo
            
        self.servo.reset()
            # Find the largest distance and its angle and return it
        if input_datas:
            to_move_distance, moving_angle = max(input_datas, key=lambda x: x[0])
            return [to_move_distance, moving_angle]
        else:
            print("No values in input datas")
    
    def can_i_keep_moving(self):
        # Reset the eye servo
        self.servo.reset()
        distance = self.lidar_sensor.get_distance_to_obstacle()
        # If the distance is less than the minimum distance the car need to stoped 
        if distance <= MINIMUM_GAP:
            return False
        else:
            return True        
            
        
def run():
    car = CarEye()
    direction = car.get_the_direction_to_move()
    print(direction)
