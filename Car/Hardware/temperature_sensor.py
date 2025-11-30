import time
import RPi.GPIO as GPIO

class DS18B20:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
    
    def reset(self):
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, 0)
        time.sleep(480e-6)  # 480us low
        GPIO.setup(self.pin, GPIO.IN)
        time.sleep(70e-6)   # 70us wait
        presence = GPIO.input(self.pin) == 0
        time.sleep(410e-6)  # 410us recovery
        return presence

    def write_bit(self, bit):
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, 0)
        if bit:
            time.sleep(10e-6)  # 10us
            GPIO.setup(self.pin, GPIO.IN)
            time.sleep(55e-6)
        else:
            time.sleep(65e-6)
            GPIO.setup(self.pin, GPIO.IN)
            time.sleep(5e-6)

    def read_bit(self):
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, 0)
        time.sleep(3e-6)
        GPIO.setup(self.pin, GPIO.IN)
        time.sleep(10e-6)
        bit = GPIO.input(self.pin)
        time.sleep(53e-6)
        return bit

    def write_byte(self, byte):
        for i in range(8):
            self.write_bit((byte >> i) & 1)

    def read_byte(self):
        value = 0
        for i in range(8):
            value |= self.read_bit() << i
        return value

    def read_temp(self):
        if not self.reset():
            raise Exception("No DS18B20 detected")
        self.write_byte(0xCC)  # Skip ROM
        self.write_byte(0x44)  # Convert T
        time.sleep(0.75)       # Wait max conversion
        if not self.reset():
            raise Exception("No DS18B20 detected")
        self.write_byte(0xCC)  # Skip ROM
        self.write_byte(0xBE)  # Read Scratchpad
        temp_l = self.read_byte()
        temp_h = self.read_byte()
        temp = ((temp_h << 8) | temp_l)
        if temp & 0x8000:      # negative
            temp = -((temp ^ 0xffff) + 1)
        return temp / 16.0

    def cleanup(self):
        GPIO.cleanup()

# ------------------------
# Example usage
# ------------------------
if __name__ == "__main__":
    sensor = DS18B20(pin=17)
    try:
        while True:
            temperature = sensor.read_temp()
            print(f"Temperature: {temperature:.2f}°C")
            time.sleep(1)
    except KeyboardInterrupt:
        sensor.cleanup()
