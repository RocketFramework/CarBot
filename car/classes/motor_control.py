from class_config import GPIO, STEPPER_PULSE_PIN, STEPPER_DIR_PIN, SERVO_CONTROL_PIN
from stepper_motor import Stepper_Motor
from servo_motor import Servo_Motor

class MotorControl:
    def __init__(self, motor_type='stepper', m_pins=None):
        GPIO.setmode(GPIO.BCM)
        self.motor_type = motor_type
        # Initialize motors based on the motor type provided
        if motor_type == 'stepper':
            self.motor_engine = Stepper_Motor()
        elif motor_type == 'servo':
            self.motor_driver = Servo_Motor(m_pins)
        else:
            raise ValueError("Unsupported motor type. Use 'stepper' or 'servo'.")

    def set_speed_direction(self, speed, direction):
        if self.motor_type == 'stepper':
            steps_left = round(1 * speed * 100)
            steps_right = round((1 - abs(direction)) * speed * 100)
            dir_left = 1 if direction >= 0 else -1
            dir_right = 1 if direction >= 0 else -1
            self.motor_engine.step(steps_left, dir_left)
        else:
            angle_left = 90 + (direction * 45)
            angle_right = 90 - (direction * 45)
            self.motor_driver.rotate(angle_left)

    def stop(self):
        if (self.motor_type == 'stepper'):
            self.motor_engine.stop()
        else:
            self.motor_driver.stop()

if __name__ == "__main__":
    # Example for Stepper Motor
    stepper_motor_control = MotorControl(
        motor_type = 'stepper',
        m_pins = (STEPPER_PULSE_PIN, STEPPER_DIR_PIN)  # Left motor: Step, Dir, Control
    )
    
    stepper_motor_control.set_speed_direction(1, 0)
    stepper_motor_control.set_speed_direction(1, -0.5)
    stepper_motor_control.set_speed_direction(1, 0.5)
    stepper_motor_control.stop()

    # Example for Servo Motor
    servo_motor_control = MotorControl(
        motor_type = 'servo',
        m_pins = SERVO_CONTROL_PIN
    )
    
    servo_motor_control.set_speed_direction(1, 0)
    servo_motor_control.set_speed_direction(1, -0.5)
    servo_motor_control.set_speed_direction(1, 0.5)
    servo_motor_control.stop()

    GPIO.cleanup()