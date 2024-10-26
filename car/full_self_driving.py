import time
import threading
from enum import Enum
from .classes.class_config import EYE_MAX_ANGLE, DRIVER_DEFAULT_ANGLE, EYE_DEFAULT_ANGLE
from .classes.car_engine import CarEngine
from .classes.car_driver import CarDriver
from .classes.car_eye import CarEye
from .classes.pca_board import PCABoard
from .car_config import MID_SPEED, MAX_SPEED
from .classes.car_eye import MoveStatus

class FullSelfDriving:
    """
    Full Self-Driving Function:
    Autonomously navigates the vehicle and reaches the destination safely.
    """
    def __init__(self):
        self.pca_board = PCABoard()
        self.carEngine = CarEngine()
        self.carDriver = CarDriver(self.pca_board)
        self.carEye = CarEye(self.pca_board)
        
        self.MID_SPEED = MID_SPEED
        self.MAX_SPEED = MAX_SPEED
        self.running = False
        self.lock = threading.Lock()
        
    def stop_loop(self):
        print("Function Called: Car Stop!")
        with self.lock:
            self.running = False
        print(f"Stop, Running: {self.running}")
    
    def cleanup(self):
        self.carEngine.cleanup()
        
    def handle_cant_move_scenario(self):
        # Get distance around car and try to find a direction
        to_move_distance, moving_angle = self.carEye.get_the_direction_to_move()
        
        if to_move_distance == 0:
            print("Function Called: Car Reverse!")
            while to_move_distance == 0:
                self.step_reverse(self.MID_SPEED)
                to_move_distance, moving_angle = self.carEye.get_the_direction_to_move()
                
            print("Function Called: Car Smart Turn And Move!")
        return moving_angle

    def reverse(self, speed):
        self.carEngine.move_reverse(speed)

    def step_reverse(self, speed):
        self.reverse(speed)
        time.sleep(1)
        self.carEngine.stop()
    
    def smart_move_speed_front(self, current_speed):
        move_status = self.carEye.can_i_keep_moving()
        time.sleep(.1)
        match move_status:
            case MoveStatus.Slow:
                current_speed = current_speed - 1
                if current_speed <= 0:
                    return 0
                return current_speed
                     
            case MoveStatus.Maintain:
                if current_speed <= MID_SPEED:
                    current_speed = current_speed + 1
                    return current_speed
                return MID_SPEED
                    
            case MoveStatus.Accelerate:    
                current_speed = current_speed + 1
                if (current_speed >= MAX_SPEED):
                    return MAX_SPEED
                return current_speed
        return current_speed
    
    def smart_turn_driver_angle_front(self, current_angle, driver_turning_angle):
        if driver_turning_angle == current_angle:
            current_angle = DRIVER_DEFAULT_ANGLE
            return DRIVER_DEFAULT_ANGLE
            
        return self.carDriver.get_front_angle(current_angle, driver_turning_angle)
    
    def smart_turn_eye_angle_front(self, current_angle, eye_turning_angle):
        if eye_turning_angle == current_angle:
            current_angle = EYE_DEFAULT_ANGLE
            return EYE_DEFAULT_ANGLE
        
        return self.carEye.get_front_angle(current_angle, eye_turning_angle)
        #return self.carEye.get_front_angle(current_angle)
      
    def drive(self):
        
        current_speed = 0
        current_driver_angle = DRIVER_DEFAULT_ANGLE
        current_eye_angle = EYE_DEFAULT_ANGLE
        driver_turning_angle = DRIVER_DEFAULT_ANGLE
        eye_turning_angle = EYE_DEFAULT_ANGLE
        try:
            with self.lock:
                self.running = True
            
            #current_speed = self.smart_move_front(current_speed=0)         
            while True:
                with self.lock:
                    if not self.running:
                        break
                    
                can_move = self.carEye.can_i_keep_moving()
                
                if can_move == MoveStatus.Stop:
                    print("Function Called: Car Stop!")
                    self.carEngine.stop()
                    current_speed = 0                 
                    to_move_distance, eye_angle = self.carEye.get_the_direction_to_move()
                    eye_turning_angle = eye_angle
                    if to_move_distance == 0:
                        eye_turning_angle = self.handle_cant_move_scenario()

                    current_speed = self.smart_move_speed_front(current_speed)
                    self.carEngine.move_forward(current_speed)
                         
                    driver_turning_angle = EYE_MAX_ANGLE - eye_turning_angle
                    current_driver_angle = DRIVER_DEFAULT_ANGLE
                    current_driver_angle = self.smart_turn_driver_angle_front(current_driver_angle, driver_turning_angle)
                    self.carDriver.set_front_angle(current_driver_angle)
                    current_eye_angle = self.smart_turn_eye_angle_front(current_eye_angle, eye_turning_angle)
                    #self.carEye.set_angle(current_eye_angle)
                    #self.car_smart_turn(angle)
                else:
                    current_speed = self.smart_move_speed_front(current_speed)
                    self.carEngine.move_forward(current_speed)
                    
                    current_driver_angle = self.smart_turn_driver_angle_front(current_driver_angle, driver_turning_angle)
                    if current_driver_angle == driver_turning_angle:
                        driver_turning_angle = DRIVER_DEFAULT_ANGLE
                    self.carDriver.set_front_angle(current_driver_angle) 
                    if current_driver_angle == DRIVER_DEFAULT_ANGLE:
                        driver_turning_angle = DRIVER_DEFAULT_ANGLE
                    
                    print(f"eye angle outside {current_eye_angle}")      
                    current_eye_angle = self.smart_turn_eye_angle_front(current_eye_angle, eye_turning_angle)
                    if current_eye_angle == eye_turning_angle:
                        eye_turning_angle = EYE_DEFAULT_ANGLE
                    print(f"eye angle outside {current_eye_angle}")                    
                    self.carEye.set_angle(current_eye_angle) 
                    if current_eye_angle == EYE_DEFAULT_ANGLE:
                        eye_turning_angle = EYE_DEFAULT_ANGLE
                    
        finally:    
            current_speed = 0
            current_driver_angle = DRIVER_DEFAULT_ANGLE
            current_eye_angle = EYE_DEFAULT_ANGLE
            self.carEngine.stop()

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
    print("Function Called: Car Stop!")
    self_drive.stop_loop()
