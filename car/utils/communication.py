import websocket
import json
from logger_config import setup_logger

# Set up the logger
logger = setup_logger(__name__)

# Function to send telemetry data over WebSocket
def send_telemetry(data, server_ip="ws://localhost:8080"):
    """
    Sends telemetry data to the remote monitoring computer.
    """
    try:
        logger.debug(f"Attempting to send telemetry data: {data}")
        
        # Establish WebSocket connection to the remote computer
        ws = websocket.WebSocket()
        ws.connect(server_ip)
        
        # Convert telemetry data to JSON and send
        ws.send(json.dumps(data))
        logger.debug("Telemetry data sent successfully.")
        
        # Close the connection after sending data
        ws.close()
    except Exception as e:
        logger.error(f"Error while sending telemetry data: {e}")

# Example function to test sending telemetry data
if __name__ == "__main__":
    example_data = {"speed": 15, "battery": 75}  # Example telemetry data
    send_telemetry(example_data)
