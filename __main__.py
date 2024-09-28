import threading
import time
import logging
import signal
import sys
from logging.handlers import RotatingFileHandler
from car.telemetry import Telemetry
from car.utils.communication import send_telemetry
from car.auto_pilot import Auto_Pilot

# Set up log rotation
log_handler = RotatingFileHandler("carbot.log", maxBytes=5000000, backupCount=5)  # 5MB per file, keep 5 backups
log_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    handlers=[log_handler, logging.StreamHandler()]
)

logger = logging.getLogger(__name__)

# Global flag to control when to stop the threads
running = True

# Gracefully handle exit signal (e.g., Ctrl + C)
def signal_handler(sig, frame):
    global running
    logger.info("Exit signal received, shutting down...")
    running = False  # Set the flag to False to stop the threads

signal.signal(signal.SIGINT, signal_handler)

# Define the car auto-driving function
def auto_run_car(car):
    while running:
        car.drive()
        logger.info("Car is driving...")
        time.sleep(0.1)
    logger.info("Car auto-driving stopped.")

# Define the telemetry function
def send_telemetry_data(telemetry):
    while running:
        data = telemetry.gather_data()
        logger.info(f"Telemetry Data: {data}")
        send_telemetry(data)
        time.sleep(1)
    logger.info("Telemetry sending stopped.")


def main():
    # Initialize telemetry and car
    telemetry = Telemetry()
    car = Auto_Pilot()

    logger.info("Starting CARBOT system...")

    # Create and start threads
    car_thread = threading.Thread(target=auto_run_car, args=(car,))
    telemetry_thread = threading.Thread(target=send_telemetry_data, args=(telemetry,))

    car_thread.start()
    telemetry_thread.start()

    # Keep the main thread alive until both threads finish
    try:
        while running:
            time.sleep(1)  # Keep the main thread alive, listening for exit signal
    except KeyboardInterrupt:
        logger.info("Shutting down CARBOT...")

    # Wait for threads to finish
    car_thread.join()
    telemetry_thread.join()

    logger.info("CARBOT system shut down gracefully.")
    
if __name__ == "__main__":
    main()