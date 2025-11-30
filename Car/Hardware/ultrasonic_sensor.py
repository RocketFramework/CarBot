import time
import RPi.GPIO as GPIO
from digitalio import Direction

class UltraSonicSensor:
    def __init__(self, trigger_pin, echo_pin, max_retries=2):
        """
        trigger_pin: MCP23017 DigitalInOut or int (Pi GPIO)
        echo_pin: int (Pi GPIO) or MCP23017 DigitalInOut
        """
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        self.max_retries = max_retries

        # Detect types
        self.trig_is_mcp = not isinstance(trigger_pin, int)
        self.echo_is_mcp = not isinstance(echo_pin, int)

        # Setup Raspberry Pi GPIO if used
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        if isinstance(trigger_pin, int):
            GPIO.setup(trigger_pin, GPIO.OUT)
        if isinstance(echo_pin, int):
            GPIO.setup(echo_pin, GPIO.IN)

        # Setup MCP pins if used
        if self.trig_is_mcp:
            self.trigger_pin.direction = Direction.OUTPUT
        if self.echo_is_mcp:
            self.echo_pin.direction = Direction.INPUT


    def get_distance(self):
        return self._get_distance_gpio()

    # ---------------------------------------
    # Case 1: TRIG and ECHO on Pi GPIO
    # ---------------------------------------
    def _get_distance_gpio(self):
        for _ in range(self.max_retries):
            GPIO.output(self.trigger_pin, GPIO.LOW)
            time.sleep(0.005)
            GPIO.output(self.trigger_pin, GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(self.trigger_pin, GPIO.LOW)

            pulse_start, pulse_end = self._measure_pulse_gpio(self.echo_pin)
            if pulse_start is None or pulse_end is None:
                continue  # retry
            duration = pulse_end - pulse_start
            return round(duration * 17150, 2)
        return 400
    # ---------------------------------------
    # Case 2: TRIG on MCP, ECHO on Pi GPIO (your setup)
    # ---------------------------------------
    def _get_distance_mcp_trig_gpio_echo(self):
        for _ in range(self.max_retries):
            # Trigger pulse
            self.trigger_pin.value = False
            time.sleep(0.005)
            self.trigger_pin.value = True
            time.sleep(0.00001)
            self.trigger_pin.value = False

            pulse_start, pulse_end = self._measure_pulse_gpio(self.echo_pin)
            duration = pulse_end - pulse_start
            if duration > 0:
                return round(duration * 17150, 2)
        return None


    # ---------------------------------------
    # Helper: measure pulse via GPIO
    # ---------------------------------------
    def _measure_pulse_gpio(self, pin):
        timeout_start = time.monotonic()
        while GPIO.input(pin) == 0:
            if time.monotonic() - timeout_start > 0.05:
                return None, None  # no pulse detected
        pulse_start = time.monotonic()

        timeout_start = time.monotonic()
        while GPIO.input(pin) == 1:
            if time.monotonic() - timeout_start > 0.05:
                return None, None  # pulse didn't end
        pulse_end = time.monotonic()

        return pulse_start, pulse_end


    def _get_distance(self):
        while True:
            time.sleep(0.015)
            dist = self._get_distance_gpio()
            if dist is not None:
                return dist
            else:
                print("Measurement failed.")