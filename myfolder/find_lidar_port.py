import serial
import os

def find_serial_port():
    possible_ports = ['/dev/serial0', '/dev/ttyAMA0', '/dev/ttyS0']
    for port in possible_ports:
        if os.path.exists(port):
            try:
                # Try opening to test if it's usable
                with serial.Serial(port, baudrate=9600, timeout=1) as ser:
                    print(f"[INFO] Using serial port: {port}")
                    return port
            except serial.SerialException as e:
                print(f"[WARNING] Port {port} found but not available: {e}")
    raise RuntimeError("❌ No usable serial ports found!")

# Example usage:
try:
    serial_port = find_serial_port()
    ser = serial.Serial(serial_port, baudrate=9600, timeout=1)
    # Use `ser` to read/write
except RuntimeError as e:
    print(e)
