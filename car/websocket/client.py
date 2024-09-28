import websocket
import json
import logging
from logging.handlers import RotatingFileHandler
import sys
import signal

# Set up log rotation for the client
log_handler = RotatingFileHandler("websocket_client.log", maxBytes=5000000, backupCount=5)
log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Set up logging
logging.basicConfig(level=logging.INFO, handlers=[log_handler])
logger = logging.getLogger(__name__)

# Callback function when a new message (telemetry) is received
def on_message(ws, message):
    try:
        telemetry_data = json.loads(message)
        logger.info(f"Received Telemetry Data: {telemetry_data}")
    except json.JSONDecodeError:
        logger.error(f"Invalid message received: {message}")

# Callback function for WebSocket error
def on_error(ws, error):
    logger.error(f"WebSocket error: {error}")

# Callback function when the WebSocket connection is closed
def on_close(ws, close_status_code, close_msg):
    logger.info("Connection closed")

# Callback function when the WebSocket connection is opened
def on_open(ws):
    logger.info("Connection opened. Ready to send telemetry data.")

# Main WebSocket client function
def start_client(server_url):
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(server_url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()

if __name__ == "__main__":
    server_url = "ws://localhost:8080"  # Replace with the actual server URL if needed

    def signal_handler(sig, frame):
        logger.info("Client is shutting down...")
        sys.exit(0)

    # Set up signal handling for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)

    start_client(server_url)
