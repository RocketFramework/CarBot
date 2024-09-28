import asyncio
import websockets
import json
import signal
import sys
from car.utils.logger_config import setup_logger
from car.car_config import WEB_SOCKET_SERVER_IP

# Set up logger
logger = setup_logger("websocket_server", log_file='websocket_server.log')

# Graceful shutdown
running = True

def signal_handler(sig, frame):
    global running
    logger.info("Shutdown signal received. Stopping server.")
    running = False

signal.signal(signal.SIGINT, signal_handler)

# WebSocket handler
async def handler(websocket, path):
    logger.info("Client connected")
    try:
        async for message in websocket:
            telemetry_data = json.loads(message)
            logger.info(f"Received Telemetry Data: {telemetry_data}")
            await websocket.send(json.dumps({"status": "received", "data": telemetry_data}))
    except websockets.exceptions.ConnectionClosed as e:
        logger.error(f"Connection closed: {e}")
    finally:
        logger.info("Client disconnected")

# Start the server
async def main():
    async with websockets.serve(handler, WEB_SOCKET_SERVER_IP, 8080):
        logger.info(f"WebSocket server is running on ws://{WEB_SOCKET_SERVER_IP}:8080")
        while running:
            await asyncio.sleep(1)

def run():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("WebSocket server is shutting down...")
        sys.exit(0)
