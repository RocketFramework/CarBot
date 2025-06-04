import RPi.GPIO as GPIO
import time
from .class_config import ULTRASONIC_TRIGGER_PIN, ULTRASONIC_ECHO_PIN
from car.memory import Memory


class UltraSonicSensor:
    def __init__(self, max_retries=2):
        self.trigger_pin = ULTRASONIC_TRIGGER_PIN
        self.echo_pin = ULTRASONIC_ECHO_PIN
        self.max_retries = max_retries
        self.carMemory = Memory()

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def get_distance(self):
        for attempt in range(self.max_retries):
            # Send trigger
            GPIO.output(self.trigger_pin, GPIO.LOW)
            time.sleep(0.005)  # Reduced wait time
            GPIO.output(self.trigger_pin, GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(self.trigger_pin, GPIO.LOW)

            # Wait for echo to go HIGH
            timeout_start = time.monotonic()
            while GPIO.input(self.echo_pin) == 0:
                if time.monotonic() - timeout_start > 0.025:  # reduced timeout
                    break
            pulse_start = time.monotonic()

            # Wait for echo to go LOW
            timeout_start = time.monotonic()
            while GPIO.input(self.echo_pin) == 1:
                if time.monotonic() - timeout_start > 0.025:
                    break
            pulse_end = time.monotonic()

            # Calculate distance
            duration = pulse_end - pulse_start
            if duration > 0:
                distance = round(duration * 17150, 2)
                self.carMemory.log("info", f"Distance Back: {distance} cm")
                return distance

        return None


def run():
    ultrasonic_sensor = UltraSonicSensor(max_retries=2)
    try:
        while True:
            distance = ultrasonic_sensor.get_distance()
            if distance is not None:
                print(f"Distance: {distance} cm")
            else:
                print("Failed to measure distance")
            time.sleep(0.05)  # sample every 50 ms
    except KeyboardInterrupt:
        print("Measurement stopped by user.")
    finally:
        GPIO.cleanup()
