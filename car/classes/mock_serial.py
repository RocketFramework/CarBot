# Mock class for serial in Windows
class MockSerial:
    def __init__(self, port=None, baudrate=None, timeout=None):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.is_open = True
        self.in_waiting = 9  # Simulate 9 bytes waiting to be read

    def open(self):
        self.is_open = True

    def close(self):
        self.is_open = False

    def read(self, size):
        # Simulate valid LIDAR data for testing
        return bytearray([0x59, 0x59, 0x12, 0x34, 0, 0, 0, 0, 0])

    def reset_input_buffer(self):
        pass