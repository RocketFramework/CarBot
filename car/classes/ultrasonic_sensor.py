import RPi.GPIO as GPIO
import time
from .class_config import ULTRASONIC_TRIGGER_PIN, ULTRASONIC_ECHO_PIN
from car.memory import Memory
from digitalio import DigitalInOut  # to help type check


class UltraSonicSensor:
    def __init__(self, max_retries=2, trigger_pin=ULTRASONIC_TRIGGER_PIN, echo_pin=ULTRASONIC_ECHO_PIN):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        self.max_retries = max_retries
        self.carMemory = Memory()

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        # Only call GPIO.setup if trigger_pin is an int (normal GPIO pin)
        if isinstance(self.trigger_pin, int):
            GPIO.setup(self.trigger_pin, GPIO.OUT)
            self.mcp_connected = False
        else:
            self.mcp_connected = True  # assume MCP23017 pin (DigitalInOut)

        GPIO.setup(self.echo_pin, GPIO.IN)

    def get_distance(self):
        return self._get_distance() if self.mcp_connected else self._get_distance_gpio()

    def _get_distance_gpio(self):
        for attempt in range(self.max_retries):
            GPIO.output(self.trigger_pin, GPIO.LOW)
            time.sleep(0.005)
            GPIO.output(self.trigger_pin, GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(self.trigger_pin, GPIO.LOW)

            timeout_start = time.monotonic()
            while GPIO.input(self.echo_pin) == 0:
                if time.monotonic() - timeout_start > 0.025:
                    break
            pulse_start = time.monotonic()

            timeout_start = time.monotonic()
            while GPIO.input(self.echo_pin) == 1:
                if time.monotonic() - timeout_start > 0.025:
                    break
            pulse_end = time.monotonic()

            duration = pulse_end - pulse_start
            if duration > 0:
                return round(duration * 17150, 2)
        return None

    def _get_distance_mcp(self):
        while True:
            self.trigger_pin.value = False
            time.sleep(0.00002)
            self.trigger_pin.value = True
            time.sleep(0.00001)
            self.trigger_pin.value = False

            timeout_start = time.monotonic()
            while GPIO.input(self.echo_pin) == 0:
                if time.monotonic() - timeout_start > 0.025:
                    break
            pulse_start = time.monotonic()

            timeout_start = time.monotonic()
            while GPIO.input(self.echo_pin) == 1:
                if time.monotonic() - timeout_start > 0.025:
                    break
            pulse_end = time.monotonic()

            duration = pulse_end - pulse_start
            if duration > 0:
                return round(duration * 17150, 2)     

            return None

    def _get_distance(self):
        while True:
            time.sleep(0.015)
            dist = self._get_distance_mcp()
            if dist is not None:
                return dist
            else:
                print("Measurement failed.")
            
            