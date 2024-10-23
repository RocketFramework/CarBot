import math
import time
from .pca_board import PCABoard
from .lida_sensor import LidarSensor
from car.car_config import MINIMUM_GAP
from .class_config import EYE_MAX_ANGLE, EYE_MIN_ANGLE, EYE_DEFAULT_ANGLE, EYE_DEFAULT_STEP
from .car_engine import CarEngine
class CarEye():
    
    def __init__(self, pca_board):
        # Custom initialization for CarEye, no call to super().__init__()
        self.eye_servo = pca_board.eye_servo
        self.lidar_sensor = LidarSensor()
        self.EYE_DEFAULT_STEP = EYE_DEFAULT_STEP
        
    def set_angle(self, angle):
        self.eye_servo.rotate(angle)
        
    # The definition will inherit the turn_left() function
    def turn_left(self, angle_step=EYE_DEFAULT_STEP) -> [bool, int]:
        self.eye_servo.angle += angle_step
        temp_angle = math.ceil(self.eye_servo.rotate(self.eye_servo.angle))
        is_moved = (temp_angle==self.eye_servo.angle)
        self.eye_servo.angle = temp_angle
        return [is_moved, self.eye_servo.angle]
    
    # The definition will inherit the turn_right() function
    def turn_right(self, angle_step=EYE_DEFAULT_STEP) -> [bool, int]:
        self.eye_servo.angle -= angle_step
        temp_angle = math.ceil(self.eye_servo.rotate(self.eye_servo.angle))
        is_moved = (temp_angle==self.eye_servo.angle)
        self.eye_servo.angle = temp_angle
        return [is_moved, self.eye_servo.angle]
    
    # The definition will turn around and return the most suitable path to go
    def get_the_direction_to_move(self) -> [int, float]:
        # Reset the servo to its default angle
        self.eye_servo.reset()
        # Create an array to store distances and angles
        input_datas = [(0, 0)]
        # Create an array to store the right turn results
        turn_data = [True, 0]      
        # Create a while is_moved == True loop
        while turn_data[0] == True:
            # Turn 10 steps right and get distance to the obstacle
            turn_data = self.turn_right()
            if turn_data[0] == True:
                distance = self.lidar_sensor.get_distance_to_obstacle()
                # Store this distance and angle in a array 
                input_datas.append((distance, turn_data[1]))
                
        # Center the eye servo 
        self.eye_servo.reset()
        # Create an array to store the left turn results
        turn_data = [True, 0]   
         
        while turn_data[0] == True:
            # Turn 10 steps left and get distance to the obstacle
            turn_data = self.turn_left()
            if turn_data[0] == True:
                distance = self.lidar_sensor.get_distance_to_obstacle()
                #print(f"distance:{distance}, angle: {turn_data[1]}")
                # Store this distance and angle in a array 
                input_datas.append((distance, turn_data[1]))
                # Center the eye servo
            
        self.eye_servo.reset()
            # Find the largest distance and its angle and return it
        if input_datas:
            to_move_distance, moving_angle = max(input_datas, key=lambda x: x[0])
            if to_move_distance < MINIMUM_GAP:
                to_move_distance = 0
                moving_angle = 0
            #print(f"Inside get direction distance:{to_move_distance},moving angle: {moving_angle}")
            return [to_move_distance, moving_angle]
        else:
            print("No values in input datas")
    
    def can_i_keep_moving(self):
        distance = self.lidar_sensor.get_distance_to_obstacle()
        time.sleep(.1)
        if distance <= MINIMUM_GAP:
            return False
        else:
            return True      
    
    def set_reset_front_angle(self, angle):        
        step = 1
        steps = abs(angle - EYE_DEFAULT_ANGLE)// step
        if angle > EYE_DEFAULT_ANGLE:
            # Start from Default angle and move until it hit the angle
            for i in range(steps):
                temp_eye_angle = EYE_DEFAULT_ANGLE + i

                if temp_eye_angle >= angle:
                    break
                self.set_angle(temp_eye_angle)
                time.sleep(.1)
                
            # Then turn back until it hit the Default angle   
            for i in range(steps):
                temp_eye_angle = angle - i
                if temp_eye_angle <= EYE_DEFAULT_ANGLE:
                    break
                self.set_angle(temp_eye_angle)
                time.sleep(.1)
        
        else:
            for i in range(steps):
                temp_eye_angle = EYE_DEFAULT_ANGLE - i
                if temp_eye_angle <= angle:
                    break
                self.set_angle(temp_eye_angle)
                time.sleep(.1)
            
            for i in range(steps):
                temp_eye_angle = angle + i
                if temp_eye_angle >= EYE_DEFAULT_ANGLE:
                    break
                self.set_angle(temp_eye_angle)
                time.sleep(.1)
                   
def run():
    car = CarEye()
    direction = car.get_the_direction_to_move()
