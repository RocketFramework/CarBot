import smbus2
import time

# --- Configuration ---
BUS = 3
PCA_ADDR = 0x40
FREQ = 50  # 50Hz standard servo

# PCA9685 registers
MODE1 = 0x00
PRESCALE = 0xFE

# --- Helper functions ---
def write_reg(reg, value):
    bus.write_byte_data(PCA_ADDR, reg, value)

def angle_to_pulse(angle, actuation_min=15, actuation_max=70, min_pulse=500, max_pulse=2500):
    """
    Map a normalized angle (0-180°) to servo's real actuation range
    actuation_min/max = actual servo physical angle
    """
    # Map 0-180 to actuation_min - actuation_max
    real_angle = actuation_min + (angle / 180.0) * (actuation_max - actuation_min)
    pulse = min_pulse + (real_angle / 180.0) * (max_pulse - min_pulse)
    return int(pulse)

def set_servo(channel, angle, actuation_min=15, actuation_max=70, min_pulse=500, max_pulse=2500):
    """
    Set servo to a normalized angle (0-180°) within its real actuation range
    """
    pulse_us = angle_to_pulse(angle, actuation_min, actuation_max, min_pulse, max_pulse)
    pulse_length = 1000000.0 / FREQ / 4096  # us per bit
    pulse = int(pulse_us / pulse_length)
    LED0_ON_L = 0x06 + 4 * channel
    bus.write_byte_data(PCA_ADDR, LED0_ON_L, 0)
    bus.write_byte_data(PCA_ADDR, LED0_ON_L + 1, 0)
    bus.write_byte_data(PCA_ADDR, LED0_ON_L + 2, pulse & 0xFF)
    bus.write_byte_data(PCA_ADDR, LED0_ON_L + 3, (pulse >> 8) & 0xFF)

# --- Initialize I2C bus ---
bus = smbus2.SMBus(BUS)

# --- Initialize PCA9685 ---
write_reg(MODE1, 0x00)
time.sleep(0.01)
prescale_val = int(25000000.0 / (4096 * FREQ) - 1)
write_reg(MODE1, 0x10)  # sleep
write_reg(PRESCALE, prescale_val)
write_reg(MODE1, 0x00)  # wake
time.sleep(0.01)

# --- Example usage ---
print("Servo test with normalized 0-180° input...")
while True:
    
    set_servo(1, int(input("Enter servo angle (0-180) for channel 1 (or 'q' to quit): ")))    # maps to physical 15° (start of actuation)

"""     set_servo(0, 0)    # maps to physical 15° (start of actuation)
    time.sleep(1)
    set_servo(0, 90)   # maps to midpoint ~42.5°
    time.sleep(1)
    set_servo(0, 180)  # maps to physical 70° (end of actuation) """
