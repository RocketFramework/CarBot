from .motor import Motor
from .class_config import GPIO, time

class Stepper_Motor_28bjy_48(Motor):
    def __init__(self, pinIn1, pinIn2, pinIn3, pinIn4):
        """ Initialize stepper motor pins. """
        super().__init__(pinIn1)
        self.__PINS = [17, 27, 22, 23]
        self.__sequence = [
            [1, 0, 0, 0],  # Step 1
            [1, 1, 0, 0],  # Step 2
            [0, 1, 0, 0],  # Step 3
            [0, 1, 1, 0],  # Step 4
            [0, 0, 1, 0],  # Step 5
            [0, 0, 1, 1],  # Step 6
            [0, 0, 0, 1],  # Step 7
            [1, 0, 0, 1]   # Step 8
        ]
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._PINS, GPIO.OUT)

    def step(self, steps, direction):
        motor_step_counter = 0
        for _ in range(steps):
            for pin in range(4):
                GPIO.output(self.__PINS[pin], self.__sequence[motor_step_counter][pin]) 
            motor_step_counter = (motor_step_counter + (1 if direction else -1)) % len(self.__sequence)
            time.sleep(self.delay)

    def stop(self):
        """ Stop the stepper motor. """
        GPIO.output(self.__PINS, GPIO.LOW)
        GPIO.cleanup()
        
if __name__ == "__main__": 
    pass   
    #Motor = Stepper_Motor(speed, direction, 4, 17, pinControl)
