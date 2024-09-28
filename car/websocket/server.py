import asyncio
import websockets
import json
import logging
from logging.handlers import RotatingFileHandler
import sys
import signal

# Set up log rotation for the server
log_handler = RotatingFileHandler("websocket_server.log", maxBytes=5000000, backupCount=5)  # 5MB per file, keep 5 backups
log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Set up logging
logging.basicConfig(level=logging.INFO, handlers=[log_handler])
logger = logging.getLogger(__name__)

async def handler(websocket, path):
    logger.info("Client connected")
    try:
        async for message in websocket:
            # Print received telemetry data
            telemetry_data = json.loads(message)
            logger.info(f"Received Telemetry Data: {telemetry_data}")

            # Optionally, you can echo the data back or send a response
            await websocket.send(json.dumps({"status": "received", "data": telemetry_data}))
    except websockets.exceptions.ConnectionClosed as e:
        logger.info(f"Connection closed: {e}")
    finally:
        logger.info("Client disconnected")

async def main():
    async with websockets.serve(handler, "localhost", 8080):
        logger.info("WebSocket server is running on ws://localhost:8080")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("WebSocket server is shutting down...")
        sys.exit(0)
