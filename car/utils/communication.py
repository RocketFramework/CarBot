import json
import websocket
from .logger_config import setup_logger


# Set up logger
logger = setup_logger("communication", log_file='communication.log')

def send_telemetry(data, server_ip):
    """
    Sends telemetry data to the WebSocket server.
    """
    try:
        logger.debug(f"Attempting to send telemetry data: {data}")
        
        # Create a WebSocket connection
        ws = websocket.create_connection(server_ip)
        ws.send(json.dumps(data))  # Send the telemetry data as a JSON string
        ws.close()  # Close the connection
        logger.debug("Telemetry data sent successfully.")
    except Exception as e:
        logger.error(f"Error while sending telemetry data: {e}")

# Example function to test sending telemetry data
if __name__ == "__main__":
    example_data = {"speed": 15, "battery": 75}  # Example telemetry data
    send_telemetry(example_data, "ws://192.168.1.100:8080")
