import random

# Mock class for serial in Windows
class MockSerial:
    def __init__(self, port=None, baudrate=None, timeout=None):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.is_open = True
        self.in_waiting = 9  # Simulate 9 bytes waiting to be read

        # Internal min and max distance settings (in meters)
        self._min_distance = 0.5
        self._max_distance = 5.0

        # Internal index for cycling through distances
        self.index = 0

        # Generate a list of distances internally
        self.distances = self._generate_distances()

    def _generate_distances(self, count=10):
        """
        Generate a list of random distances within the internally set range.
        """
        return [random.uniform(self._min_distance, self._max_distance) for _ in range(count)]

    def open(self):
        self.is_open = True

    def close(self):
        self.is_open = False

    def read(self, size):
        if not self.distances:
            return bytearray([0x59, 0x59, 0, 0, 0, 0, 0, 0, 0])

        # Get the next distance from the internal array
        distance = self.distances[self.index]

        # Update index to move to the next distance, reset if at the end of the list
        self.index = (self.index + 1) % len(self.distances)

        # Convert the distance to two bytes (assuming the LIDAR sends 16-bit distance values)
        high_byte = int(distance) >> 8  # High byte of the distance
        low_byte = int(distance) & 0xFF  # Low byte of the distance

        # Simulate a valid LIDAR packet (header + distance)
        return bytearray([0x59, 0x59, high_byte, low_byte, 0, 0, 0, 0, 0])

    def reset_input_buffer(self):
        pass
    
if __name__ == "__main__":
    # Example usage
    mock_serial = MockSerial()

    # Simulate reading distances
    for _ in range(10):  # Simulate more reads than distances to see the cycling
        print(mock_serial.read(9))
