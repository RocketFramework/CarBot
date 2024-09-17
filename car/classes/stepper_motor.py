from motor import Motor
from config import GPIO, time


class Stepper_Motor(Motor):
    def __init__(self, speed, direction, pinStep, pinDir, pinControl):
        """ Initialize stepper motor pins. """
        super().__init__(pinControl)
        self.pinStep = pinStep
        self.pinDir = pinDir
        GPIO.setup(self.pinStep, GPIO.OUT)
        GPIO.setup(self.pinDir, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pinStep, 1000)  # Setup PWM for step pin
        self.pwm.start(0)
        GPIO.output(self.pinControl, GPIO.HIGH)

    def step(self, steps, direction):
        """ Control the stepper motor. Steps and direction (1 or -1). """
        GPIO.output(self.pinDir, GPIO.HIGH if direction > 0 else GPIO.LOW)
        for _ in range(steps):
            GPIO.output(self.pinStep, GPIO.HIGH)
            time.sleep(0.001)  # Small delay for stepping
            GPIO.output(self.pinStep, GPIO.LOW)
            time.sleep(0.001)

    def stop(self):
        """ Stop the stepper motor. """
        GPIO.output(self.pinStep, GPIO.LOW)