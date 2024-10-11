import RPi.GPIO as GPIO
import time

# Suppress GPIO warnings
GPIO.setwarnings(False)

# Use Broadcom pin numbering
GPIO.setmode(GPIO.BCM)

# Define GPIO pins
RPWM_PIN = 18  # GPIO18 (Pin 12) - Right PWM
LPWM_PIN = 19  # GPIO19 (Pin 35) - Left PWM
REN_PIN  = 23  # GPIO23 (Pin 16) - Right Enable
LEN_PIN  = 24  # GPIO24 (Pin 18) - Left Enable

# Set up GPIO pins
GPIO.setup(RPWM_PIN, GPIO.OUT)
GPIO.setup(LPWM_PIN, GPIO.OUT)
GPIO.setup(REN_PIN, GPIO.OUT)
GPIO.setup(LEN_PIN, GPIO.OUT)

# Initialize PWM on RPWM and LPWM
PWM_FREQ = 1000  # Frequency in Hz

rpwm = GPIO.PWM(RPWM_PIN, PWM_FREQ)
lpwm = GPIO.PWM(LPWM_PIN, PWM_FREQ)

rpwm.start(0)  # Start with 0% duty cycle
lpwm.start(0)

def set_motor_forward(speed):
    """
    Sets the motor to move forward.
    :param speed: Speed percentage (0 to 100)
    """
    GPIO.output(REN_PIN, GPIO.HIGH)  # Enable Right
    GPIO.output(LEN_PIN, GPIO.HIGH1)   # Disable Left
    rpwm.ChangeDutyCycle(speed)
    lpwm.ChangeDutyCycle(0)
    print(f"Motor moving forward at {speed}% speed.")

def set_motor_reverse(speed):
    """
    Sets the motor to move in reverse.
    :param speed: Speed percentage (0 to 100)
    """
    GPIO.output(REN_PIN, GPIO.HIGH)   # Disable Right
    GPIO.output(LEN_PIN, GPIO.HIGH)  # Enable Left
    lpwm.ChangeDutyCycle(speed)
    rpwm.ChangeDutyCycle(0)
    print(f"Motor moving in reverse at {speed}% speed.")

def stop_motor():
    """
    Stops the motor.
    """
    GPIO.output(REN_PIN, GPIO.LOW)   # Disable Right
    GPIO.output(LEN_PIN, GPIO.LOW)   # Disable Left
    rpwm.ChangeDutyCycle(0)
    lpwm.ChangeDutyCycle(0)
    print("Motor stopped.")

def cleanup():
    """
    Stops PWM and cleans up GPIO settings.
    """
    rpwm.stop()
    lpwm.stop()
    GPIO.cleanup()
    print("GPIO cleanup completed.")

# Example Usage
if __name__ == "__main__":
    try:
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
                    set_motor_forward(speed)
                else:
                    print("Invalid speed. Please enter a value between 0 and 100.")
            elif choice == '2':
                speed = float(input("Enter speed percentage (0-100): "))
                if 0 <= speed <= 100:
                    set_motor_reverse(speed)
                else:
                    print("Invalid speed. Please enter a value between 0 and 100.")
            elif choice == '3':
                stop_motor()
            elif choice == '4':
                stop_motor()
                break
            else:
                print("Invalid choice. Please select a valid option.")

    except KeyboardInterrupt:
        print("\nInterrupted by user.")

    finally:
        cleanup()
