import time
from typing import Tuple
import math
from Car.config import EYE_DEFAULT_ANGLE, TURN_STEP_SIZE, SLEEP_TIME, HIGH_GAP, MID_GAP, EYE_DEFAULT_STEP
from Car.Hardware.pca_board import PCA9685
from Car.Hardware.lidar_sensor import TF_Luna
from Car.Hardware.mcp_board import MCP23017
from enum import Enum

class SpeedList(Enum):
    Stop = 0
    Slow = 1
    Maintain = 2
    Accelerate = 3
class CarEye:
    def __init__(self, pca_board, logger) -> None:
        self.eye_servo = pca_board.eye_servo
        self.lidar_sensor = TF_Luna()
        self.sensorBoard = MCP23017()
        self.logger = logger
        
    def set_angle(self, angle:int):
        self.current_eye_angle = self.eye_servo.rotate(angle)

    def get_distance(self):
        return self.sensorBoard.left_edge_sensor.get_distance(), self.lidar_sensor.get_distance_to_obstacle(), self.sensorBoard.right_edge_sensor.get_distance()
    
    def turn_right(self, angle_step=EYE_DEFAULT_STEP) -> Tuple[bool, int]:
        self.eye_servo.angle -= angle_step
        temp_angle = math.ceil(self.eye_servo.rotate(self.eye_servo.angle))
        is_moved = (temp_angle == self.eye_servo.angle)
        self.eye_servo.angle = temp_angle
        return [is_moved, self.eye_servo.angle]
    
    def turn_left(self, angle_step=EYE_DEFAULT_STEP) -> Tuple[bool, int]:
        self.eye_servo.angle += angle_step
        temp_angle = math.ceil(self.eye_servo.rotate(self.eye_servo.angle))
        is_moved = (temp_angle == self.eye_servo.angle)
        self.eye_servo.angle = temp_angle
        return [is_moved, self.eye_servo.angle]
    
    def smart_straight(self, current_angle:int, turning_angle:int):
        if turning_angle == EYE_DEFAULT_ANGLE:
            if turning_angle > current_angle:
                current_angle = int(current_angle + TURN_STEP_SIZE)
                return current_angle

            elif turning_angle < current_angle:
                current_angle = int(current_angle - TURN_STEP_SIZE)

                return current_angle

            return current_angle
        else:
            return turning_angle
        

    def smart_speed_monitor(self, L_MINIMUM_GAP:int, C_MINIMUM_GAP:int, R_MINIMUM_GAP:int):
        L_MID_GAP = MID_GAP * 100
        R_MID_GAP = MID_GAP * 100
        last_reading_time = 0
        last_left_read = 0
        last_right_read = 0
        current_time = time.time()
        
        if current_time - last_reading_time >= SLEEP_TIME:
            C = self.lidar_sensor.get_distance_to_obstacle()
            last_reading_time = current_time
        
        if current_time - last_left_read >= SLEEP_TIME:
            L = self.sensorBoard.left_edge_sensor.get_distance()
            last_left_read = current_time

        if current_time - last_right_read >= SLEEP_TIME:
            R = self.sensorBoard.right_edge_sensor.get_distance()
            last_right_read = current_time

        L, C, R = L, C, R
        self.logger.log("info", f"Distances - Left: {L}, Center: {C}, Right: {R}")

        if C > HIGH_GAP and L > HIGH_GAP and R > HIGH_GAP:
            return SpeedList.Accelerate
        elif HIGH_GAP >= C > MID_GAP and HIGH_GAP >= L > MID_GAP and HIGH_GAP >= R > MID_GAP:
            return SpeedList.Maintain
        elif MID_GAP >= C > C_MINIMUM_GAP and L_MID_GAP >= L > L_MINIMUM_GAP and R_MID_GAP >= R > R_MINIMUM_GAP:
            return SpeedList.Slow
        elif C <= C_MINIMUM_GAP or L <= L_MINIMUM_GAP or R <= R_MINIMUM_GAP:
            return SpeedList.Stop
        
        return SpeedList.Maintain
    
    def get_moving_direction(self):
        self.eye_servo.reset()
        distances = [(0, 0)]
        servo_status = [True, 0]

        while servo_status[0] == True:
            servo_status = self.turn_right()
            if servo_status[0] == True:
                distance = self.lidar_sensor.get_distance_to_obstacle()
                distances.append((distance, servo_status[1]))
                time.sleep(.001)

        self.eye_servo.reset()
        servo_status = [True, 0]

        while servo_status[0] == True:
            servo_status = self.turn_left()
            if servo_status[0] == True:
                distance = self.lidar_sensor.get_distance_to_obstacle()
                distances.append((distance, servo_status[1]))
                time.sleep(.001)

        self.eye_servo.reset()

        if distances:
            to_move_distance, moving_angle = max(
                distances, key=lambda x: x[0])
            return [to_move_distance, moving_angle]
        else:
            print("No values in distances")
