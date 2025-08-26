import RPi.GPIO as GPIO
import time

class DcMotor:
    def __init__(self, RPWM, LPWM, REN, LEN):
        # Always set mode first thing
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Correct pin mapping
        self.RPWM_PIN = RPWM
        self.LPWM_PIN = LPWM
        self.REN_PIN  = REN
        self.LEN_PIN  = LEN

        # Set up pins
        GPIO.setup(self.RPWM_PIN, GPIO.OUT)
        GPIO.setup(self.LPWM_PIN, GPIO.OUT)
        GPIO.setup(self.REN_PIN, GPIO.OUT)
        GPIO.setup(self.LEN_PIN, GPIO.OUT)

        # PWM setup
        PWM_FREQ = 1000
        self.rpwm = GPIO.PWM(self.RPWM_PIN, PWM_FREQ)
        self.lpwm = GPIO.PWM(self.LPWM_PIN, PWM_FREQ)
        self.rpwm.start(0)
        self.lpwm.start(0)

    def ensure_mode(self):
        """Make sure pin mode is always set before output."""
        if GPIO.getmode() is None:
            GPIO.setmode(GPIO.BCM)

    def set_motor_forward(self, speed):
        self.ensure_mode()
        GPIO.output(self.REN_PIN, GPIO.HIGH)
        GPIO.output(self.LEN_PIN, GPIO.HIGH)
        self.rpwm.ChangeDutyCycle(speed)
        self.lpwm.ChangeDutyCycle(0)
        if __name__ == "__main__":
            print(f"Motor moving forward at {speed}% speed.")

    def set_motor_reverse(self, speed):
        self.ensure_mode()
        GPIO.output(self.REN_PIN, GPIO.HIGH)
        GPIO.output(self.LEN_PIN, GPIO.HIGH)
        self.lpwm.ChangeDutyCycle(speed)
        self.rpwm.ChangeDutyCycle(0)
        if __name__ == "__main__":
            print(f"Motor moving in reverse at {speed}% speed.")

    def stop_motor(self):
        self.ensure_mode()
        GPIO.output(self.REN_PIN, GPIO.LOW)
        GPIO.output(self.LEN_PIN, GPIO.LOW)
        self.rpwm.ChangeDutyCycle(0)
        self.lpwm.ChangeDutyCycle(0)
        print("Motor stopped.")

    def cleanup(self):
        self.rpwm.stop()
        self.lpwm.stop()
        GPIO.cleanup()
        # print("GPIO cleanup completed.")

if __name__ == "__main__":
    try:
        dcmotor = DcMotor(18, 19, 23, 24)
        while True:
            print("\nSelect Motor Control Option:")
            print("1. Move Forward")
            print("2. Move Reverse")
            print("3. Stop")
            print("4. Exit")
            choice = input("Enter choice (1-4): ")

            if choice == '1':
                speed = float(input("Enter speed percentage (0-100): "))
                if 0 <= speed <= 100:
                    dcmotor.set_motor_forward(speed)
                    time.sleep(1)
                else:
                    print("Invalid speed. Please enter a value between 0 and 100.")
            elif choice == '2':
                speed = float(input("Enter speed percentage (0-100): "))
                if 0 <= speed <= 100:
                    dcmotor.set_motor_reverse(speed)
                else:
                    print("Invalid speed. Please enter a value between 0 and 100.")
            elif choice == '3':
                dcmotor.stop_motor()
            elif choice == '4':
                dcmotor.stop_motor()
                break
            else:
                print("Invalid choice. Please select a valid option.")
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    finally:
        dcmotor.cleanup()
