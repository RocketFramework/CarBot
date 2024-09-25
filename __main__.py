# This is where you'd define the main entry point for your project.

from car.classes.motor import Motor
from car.classes.stepper_motor import Stepper_Motor


def main():
    print("Running the main application...")
    motor = Motor(10)
    stepper_motor = Stepper_Motor()
    
    # You can run your main application logic here
    motor.stop()
    stepper_motor.cleanup()

if __name__ == "__main__":
    main()