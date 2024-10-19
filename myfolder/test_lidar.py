import time
import busio
import board
from adafruit_bus_device.i2c_device import I2CDevice

i2c = busio.I2C(board.SCL, board.SDA)
device_address = 0x40  # Adjust as necessary

device = I2CDevice(i2c, device_address)

def read_device():
    try:
        with device:
            # Example read operation; replace with your specific logic
            data = bytearray(2)
            device.readinto(data)
            print(f"Data read: {data}")
            return data
    except ValueError as e:
        print(f"Error reading device: {e}")
        return None

# Attempt to read from the device multiple times
for _ in range(5):
    result = read_device()
    if result is not None:
        break  # Exit loop if read is successful
    time.sleep(1)  # Wait before retrying
else:
    print("Failed to read from the I2C device after multiple attempts.")
