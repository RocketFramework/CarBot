from navio2.pwm import PWM
import time

# Initialize PWM on channel 0
servo = PWM(0)
servo.initialize()
servo.set_period(20000)  # 20 ms period (50 Hz)
servo.enable()

def set_servo_angle(angle):
    """
    Set servo angle in degrees (0-180).
    Converts angle to pulse width in microseconds.
    """
    min_us = 1000  # 0 degrees
    max_us = 2000  # 180 degrees
    pulse_us = min_us + (max_us - min_us) * (angle / 180)
    servo.set_duty_cycle(pulse_us)
    print(f"Servo angle set to {angle}° ({pulse_us} µs)")

# Example usage
set_servo_angle(0)      # Turn to 0 degrees
time.sleep(1)
set_servo_angle(90)     # Turn to 90 degrees
time.sleep(1)
set_servo_angle(180)    # Turn to 180 degrees
time.sleep(1)
