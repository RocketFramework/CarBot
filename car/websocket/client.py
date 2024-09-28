import websocket
import json
import threading
import time
import signal
from utils.logger_config import setup_logger

# Set up logger
logger = setup_logger("websocket_client", log_file='websocket_client.log')

running = True

def signal_handler(sig, frame):
    global running
    logger.info("Shutdown signal received. Stopping client.")
    running = False

signal.signal(signal.SIGINT, signal_handler)

# Callback functions for WebSocket
def on_message(ws, message):
    try:
        telemetry_data = json.loads(message)
        logger.info(f"Received Telemetry Data: {telemetry_data}")
    except json.JSONDecodeError:
        logger.error(f"Invalid message received: {message}")

def on_error(ws, error):
    logger.error(f"WebSocket error: {error}")

def on_close(ws, close_status_code, close_msg):
    logger.info("Connection closed")

def on_open(ws):
    logger.info("Connection opened. Ready to receive telemetry data.")

# Main client function
def start_client(server_url):
    ws = websocket.WebSocketApp(server_url,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever()

if __name__ == "__main__":
    server_url = "ws://localhost:8080"
    client_thread = threading.Thread(target=start_client, args=(server_url,))
    client_thread.start()

    try:
        while running:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Client shutting down...")
    client_thread.join()
