import time
import threading
from .classes.class_config import EYE_MAX_ANGLE
from .classes.car_engine import CarEngine
from .classes.car_driver import CarDriver
from .classes.car_eye import CarEye
from .classes.pca_board import PCABoard
from .car_config import SPEED


class FullSelfDriving:
    """
    Full Self-Driving Function:
    Autonomously navigates the vehicle and reache the destination safely.
    """
    def __init__(self):
        self.pca_board = PCABoard()
        self.carEngine = CarEngine()
        self.carDriver = CarDriver(self.pca_board)
        self.carEye = CarEye(self.pca_board)
        
        self.SPEED = SPEED
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
            
        # Get distance around car
        to_move_distance, moving_angle = self.carEye.get_the_direction_to_move()
        if to_move_distance == 0:
            # TODO: Get rear distance to obstacle
            
            # Slowly move the car Reverse
            self.step_reverse(self.SPEED)
            to_move_distance, moving_angle = self.carEye.get_the_direction_to_move()
            # While reversing get the distance around
            while to_move_distance == 0:
                self.step_reverse(self.SPEED)
                to_move_distance, moving_angle = self.carEye.get_the_direction_to_move()
            return moving_angle
        else:
            return moving_angle

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

            while True:
                with self.lock:
                    if not self.running:
                        break

                if not can_move:
                    #print("I cant Move")
                    self.carEngine.stop()
                    to_move_distance, angle = self.carEye.get_the_direction_to_move()
                    if to_move_distance == 0:
                        angle = self.handle_cant_move_scenario()
                        
                    # Move the car forward
                    self.carEngine.move_forward(self.SPEED)  
                    # TODO: Keep geting the distance to the obstacle
                    
                    # Do the smart turn
                    self.car_smart_turn(angle) 
                else:
                    self.carEngine.move_forward(self.SPEED)               
                can_move = self.carEye.can_i_keep_moving()
        finally:    
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

        