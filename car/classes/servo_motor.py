from motor import Motor
from config import GPIO, time

class Servo_Motor(Motor):
    def __init__(self, pinControl):
        """ Initialize servo motor pin and PWM. """
        super().__init__(pinControl)
        self.pwm = GPIO.PWM(self.pinControl, 50)  # 50 Hz frequency for servo
        self.pwm.start(0)

    def rotate(self, angle):
        """ Control servo motor by rotating it to a specific angle (0-180 degrees). """
        duty_cycle = 2 + (angle / 18)  # Convert angle to duty cycle (2-12)
        GPIO.output(self.pinControl, True)
        self.pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(self.delay(delay=None))  # Wait for the servo to move to position
        GPIO.output(self.pinControl, False)
        self.pwm.ChangeDutyCycle(0)

    def stop(self):
        """ Stop the servo motor by setting the PWM duty cycle to 0. """
        self.pwm.ChangeDutyCycle(0)
