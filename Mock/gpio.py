class MockGPIO:
    BCM = "BCM"
    BOARD = "BOARD"
    OUT = "OUT"
    IN = "IN"
    HIGH = True
    LOW = False
    PINS = {}

    mode = None

    @staticmethod
    def setmode(mode):
        MockGPIO.mode = mode

    @staticmethod
    def setup(pin, mode):
        MockGPIO.PINS[pin] = {'mode': mode, 'state': None}

    @staticmethod
    def output(pin, state):
        if pin in MockGPIO.PINS and MockGPIO.PINS[pin]['mode'] == MockGPIO.OUT:
            MockGPIO.PINS[pin]['state'] = state

    @staticmethod
    def input(pin):
        if pin in MockGPIO.PINS and MockGPIO.PINS[pin]['mode'] == MockGPIO.IN:
            return MockGPIO.PINS[pin]['state']
        return None

    @staticmethod
    def cleanup():
        MockGPIO.PINS.clear()

    @staticmethod
    def PWM(pin, frequency):
        # Return a mock PWM object
        return MockPWM(pin, frequency)


class MockPWM:
    def __init__(self, pin, frequency):
        self.pin = pin
        self.frequency = frequency
        self.duty_cycle = 0
        self.is_started = False

    def start(self, duty_cycle):
        self.duty_cycle = duty_cycle
        self.is_started = True
        print(f"Starting PWM on pin {self.pin} with duty cycle {duty_cycle}%")

    def ChangeDutyCycle(self, duty_cycle):
        self.duty_cycle = duty_cycle
        print(f"Changing PWM duty cycle on pin {self.pin} to {duty_cycle}%")

    def ChangeFrequency(self, frequency):
        self.frequency = frequency
        print(f"Changing PWM frequency on pin {self.pin} to {frequency}Hz")

    def stop(self):
        self.is_started = False
        print(f"Stopping PWM on pin {self.pin}")