import RPi.GPIO as GPIO
import time

class DcMotor:
    def __init__(self):
        # Use Broadcom pin numbering
        GPIO.setmode(GPIO.BCM)

        # Define GPIO pins
        self.RPWM_PIN = 18  # GPIO18 (Pin 12) - Right PWM
        self.LPWM_PIN = 19  # GPIO19 (Pin 35) - Left PWM
        self.REN_PIN  = 23  # GPIO23 (Pin 16) - Right Enable
        self.LEN_PIN  = 24  # GPIO24 (Pin 18) - Left Enable

        # Set up GPIO pins
        GPIO.setup(self.RPWM_PIN, GPIO.OUT)
        GPIO.setup(self.LPWM_PIN, GPIO.OUT)
        GPIO.setup(self.REN_PIN, GPIO.OUT)
        GPIO.setup(self.LEN_PIN, GPIO.OUT)
        print("set all pins to output mode")
        # Initialize PWM on RPWM and LPWM
        PWM_FREQ = 1000  # Frequency in Hz

        self.rpwm = GPIO.PWM(self.RPWM_PIN, PWM_FREQ)
        self.lpwm = GPIO.PWM(self.LPWM_PIN, PWM_FREQ)

        self.rpwm.start(0)  # Start with 0% duty cycle
        self.lpwm.start(0)

    def set_motor_forward(self, speed):
        """
        Sets the motor to move forward.
        :param speed: Speed percentage (0 to 100)
        """
        GPIO.output(self.REN_PIN, GPIO.HIGH)  # Enable Right
        GPIO.output(self.LEN_PIN, GPIO.HIGH)   # Disable Left
        self.rpwm.ChangeDutyCycle(speed)
        self.lpwm.ChangeDutyCycle(0)
        print(f"Motor moving forward at {speed}% speed.")

    def set_motor_reverse(self, speed):
        """
        Sets the motor to move in reverse.
        :param speed: Speed percentage (0 to 100)
        """
        GPIO.output(self.REN_PIN, GPIO.HIGH)   # Disable Right
        GPIO.output(self.LEN_PIN, GPIO.HIGH)  # Enable Left
        self.lpwm.ChangeDutyCycle(speed)
        self.rpwm.ChangeDutyCycle(0)
        print(f"Motor moving in reverse at {speed}% speed.")

    def stop_motor(self):
        """
        Stops the motor.
        """
        GPIO.output(self.REN_PIN, GPIO.LOW)   # Disable Right
        GPIO.output(self.LEN_PIN, GPIO.LOW)   # Disable Left
        self.rpwm.ChangeDutyCycle(0)
        self.lpwm.ChangeDutyCycle(0)
        print("Motor stopped.")

    def cleanup(self):
        """
        Stops PWM and cleans up GPIO settings.
        """
        self.rpwm.stop()
        self.lpwm.stop()
        GPIO.cleanup()
        print("GPIO cleanup completed.")

# Example Usage
if __name__ == "__main__":
    try:
        dcmotor = DcMotor()
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
