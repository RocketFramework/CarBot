from motor import Motor
from class_config import GPIO, time, STEPPER_PULSE_PIN, STEPPER_DIR_PIN, STEPPER_STEPS
from enum import Enum

class Direction(Enum):
    FORWARD = 1
    REVERSE = -1

class Stepper_Motor(Motor):
    def __init__(self):
        """ Initialize stepper motor pins. """
        super().__init__(STEPPER_PULSE_PIN)
        self.pinDir = STEPPER_DIR_PIN
        GPIO.setup(self.pinDir, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pinControl, 1000)  # Setup PWM for step pin
        self.pwm.start(0)
        GPIO.output(self.pinControl, GPIO.HIGH)

    def step(self, steps: int, direction: Direction):
        """ Control the stepper motor. Steps and direction (1 or -1). """
        GPIO.output(self.pinDir, GPIO.HIGH if direction > 0 else GPIO.LOW)
        for _ in range(steps):
            GPIO.output(self.pinControl, GPIO.HIGH)
            time.sleep(self.Delay)  # Small delay for stepping
            GPIO.output(self.pinControl, GPIO.LOW)
            time.sleep(self.Delay)

    def stop(self):
        """ Stop the stepper motor. """
        GPIO.output(self.pinControl, GPIO.LOW)
        GPIO.output(self.pinStep, GPIO.LOW)
        
    def cleanup(self):
        GPIO.cleanup()
        
if __name__ == "__main__": 
    pass   
    #Motor = Stepper_Motor(speed, direction, 4, 17, pinControl)