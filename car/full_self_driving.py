import time
import threading
from enum import Enum
from .classes.class_config import EYE_MAX_ANGLE, DRIVER_DEFAULT_ANGLE, EYE_DEFAULT_ANGLE
from .classes.car_engine import CarEngine
from .classes.car_driver import CarDriver
from .classes.car_eye import CarEye
from .classes.pca_board import PCABoard
from .car_config import MINIMUM_SPEED, MID_SPEED, MAX_SPEED, REVERSE_SPEED, GEAR_SHIFTING_TIME, GEAR_INCRECEMENT_VALUE, REVERSE_SLEEP_TIME
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
        self.GEAR_INCRECEMENT_VALUE = GEAR_INCRECEMENT_VALUE
        
        self.running = False
        self.turning = bool()
        self.lock = threading.Lock()
        self.systemState = list
        
    def stop_loop(self):
        print("Function Called: Car Stop!")
        with self.lock:
            self.running = False

        print(f"Stop, Running: {self.running}")
        
    def cleanup(self):
        self.carEngine.cleanup()
        self.systemState = "Cleaned Up"
        
    def handle_cant_move_scenario(self, MINIMUM_GAP):
        # Get distance around car and try to find a direction

        distance = self.carEye.get_distance_front()
        fist_time = True
        if distance <= MINIMUM_GAP:
            self.carEngine.stop()
            self.pca_board.reset()
            print("Function Called: Car Reverse!")
            self.step_reverse(REVERSE_SPEED)
            while True:
                with self.lock:
                    if not self.running:
                        break
                distance = self.carEye.get_distance_front()
                if distance >= MINIMUM_GAP:
                    break
                
            self.carEngine.stop()   
            distance, moving_angle = self.carEye.get_the_direction_to_move(MINIMUM_GAP)
            print("Function Called: Car Smart Turn And Move!")
        else:
            moving_angle = EYE_DEFAULT_ANGLE
        
        return moving_angle

    def reverse(self, speed):
        self.carEngine.move_reverse(speed)
        time.sleep(1)
        
    def step_reverse(self, speed):
        self.reverse(speed)
        
    def smart_move_speed_front(self, current_speed, MINIMUM_GAP):
        move_status = self.carEye.can_i_keep_moving(MINIMUM_GAP)
        time.sleep(GEAR_SHIFTING_TIME)   
        match move_status:
            case MoveStatus.Stop:
                return 0 
            
            case MoveStatus.Slow:
                if current_speed > MINIMUM_SPEED: 
                    current_speed = max(current_speed -self.GEAR_INCRECEMENT_VALUE, MINIMUM_SPEED)
                elif  20 > current_speed >= 0:
                    current_speed = min(current_speed +self.GEAR_INCRECEMENT_VALUE, MINIMUM_SPEED)
                return current_speed
            
            case MoveStatus.Maintain:
                if current_speed < 20: 
                    current_speed = min(current_speed + self.GEAR_INCRECEMENT_VALUE, MINIMUM_SPEED)
                elif 20 <= current_speed < MID_SPEED:
                    current_speed = min(current_speed + 2, MID_SPEED)
                return current_speed
            
            case MoveStatus.Accelerate:
                if current_speed < MINIMUM_SPEED:
                    current_speed = min(current_speed + 2, 50)
                elif MINIMUM_SPEED <= current_speed < MID_SPEED:
                    current_speed = min(current_speed + 5, MAX_SPEED)
                elif MID_SPEED <= current_speed <= MAX_SPEED:
                    current_speed = min(current_speed + 7, MAX_SPEED)
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
      
    def drive(self, MINIMUM_GAP):
        
        current_speed = 0
        current_driver_angle = DRIVER_DEFAULT_ANGLE
        current_eye_angle = EYE_DEFAULT_ANGLE
        driver_turning_angle = DRIVER_DEFAULT_ANGLE
        eye_turning_angle = EYE_DEFAULT_ANGLE
        try:
            with self.lock:
                self.running = True
                

            while True:
                
                with self.lock:
                    if not self.running:
                        break

                current_speed = self.smart_move_speed_front(current_speed, MINIMUM_GAP)
                if current_speed == 0:
                    print("Function Called: Car Stop!")
                    self.carEngine.stop()
                    current_speed = 0              
                    distance = self.carEye.get_distance_front()
                    if distance <= MINIMUM_GAP:
                        print("Function Called: handle_cant_move_scenario!")
                        eye_turning_angle = self.handle_cant_move_scenario(MINIMUM_GAP)

                    current_speed = self.smart_move_speed_front(current_speed, MINIMUM_GAP)
                    self.carEngine.move_forward(current_speed)
                         
                    driver_turning_angle = EYE_MAX_ANGLE - eye_turning_angle
                    current_driver_angle = self.smart_turn_driver_angle_front(current_driver_angle, driver_turning_angle)
                    self.carDriver.set_front_angle(current_driver_angle)
                    current_eye_angle = self.smart_turn_eye_angle_front(current_eye_angle, eye_turning_angle)
                    self.carEye.set_angle(current_eye_angle)
                    #self.carEye.set_angle(current_eye_angle)
                elif 0 < current_speed <= 20:
                    self.carEngine.move_forward(current_speed)
                    if not self.turning:
                        distance, moving_angle = self.carEye.get_the_direction_to_move(MINIMUM_GAP)
                    eye_turning_angle = moving_angle
                    driver_turning_angle = EYE_MAX_ANGLE - eye_turning_angle
                    current_driver_angle = self.smart_turn_driver_angle_front(current_driver_angle, driver_turning_angle)
                    self.carDriver.set_front_angle(current_driver_angle)
                    current_eye_angle = self.smart_turn_eye_angle_front(current_eye_angle, eye_turning_angle)
                    self.carEye.set_angle(current_eye_angle)
                    
                    if current_driver_angle == driver_turning_angle and current_eye_angle == eye_turning_angle:
                        
                        while current_driver_angle != DRIVER_DEFAULT_ANGLE and current_eye_angle != EYE_DEFAULT_ANGLE:
                            self.turning = True
                            current_speed = self.smart_move_speed_front(current_speed, MINIMUM_GAP)
                            self.carEngine.move_forward(current_speed)
                            if current_speed == 0:
                                break
                            current_driver_angle = self.smart_turn_driver_angle_front(current_driver_angle,
                                                                                        DRIVER_DEFAULT_ANGLE)
                            self.carDriver.set_front_angle(current_driver_angle)
                            current_eye_angle = self.smart_turn_eye_angle_front(current_eye_angle,
                                                                                EYE_DEFAULT_ANGLE)
                            self.carEye.set_angle(current_eye_angle)
                            if current_driver_angle == DRIVER_DEFAULT_ANGLE and current_eye_angle == EYE_DEFAULT_ANGLE:
                                break
                        self.turning = False
                    else:
                        self.turning = True
                        
                else:
                    # current_speed = self.smart_move_speed_front(current_speed)
                    self.carEngine.move_forward(current_speed)

                    current_driver_angle = self.smart_turn_driver_angle_front(current_driver_angle, driver_turning_angle)
                    if current_driver_angle == driver_turning_angle:
                        driver_turning_angle = DRIVER_DEFAULT_ANGLE
                    self.carDriver.set_front_angle(current_driver_angle) 
                    if current_driver_angle == DRIVER_DEFAULT_ANGLE:
                        driver_turning_angle = DRIVER_DEFAULT_ANGLE
                    
                    #print(f"eye angle outside {current_eye_angle}")      
                    current_eye_angle = self.smart_turn_eye_angle_front(current_eye_angle, eye_turning_angle)
                    if current_eye_angle == eye_turning_angle:
                        eye_turning_angle = EYE_DEFAULT_ANGLE
                    #print(f"eye angle outside {current_eye_angle}")                    
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
