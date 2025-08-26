# CarBot

CarBot is a project designed to create an autonomous self-driving vehicle using Raspberry Pi and other hardware components.

## Features
- Autonomous driving capabilities.
- Obstacle detection and avoidance.
- Real-Time log streaming via telemetry

## Requirements
- Raspberry Pi (any compatible model)                                       - x1
- IBT2 Motor Driver Module                                                  - x2
- HCSR04 Ultrasonic sensor                                                  - x3
- Raspberry Pi Arducam Module                                               - x1
- 12V 7A+ Sealed Lead Acid Battery                                          - x1
- Python 3.10+ and necessary libraries as mentioned in reuirements.txt

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/rocketframework/CarBot.git
    ```
2. Navigate to the project directory:
    ```bash
    cd CarBot
    ```
3. Install the required Python libraries:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. Assemble the hardware components as per the provided schematic.
2. Boot on the Raspberry Pi and connect to Wi-Fi
3. Connect a seperate computer to the same Wi-Fi Network
4. Get the IP address o the external computer and add it to car_config.py (replace 127.0.0.1 with the new IP)
2. Run the run_server.py in the external computer:
    ```bash
    python3 /path/to/your/CarBot/run_server.py
    ```
3. Run the run_client.py in the terminal of the Raspberry Pi
    ```bash
    python3 /path/to/your/CarBot/run_client.py
    ```
4. Wait for the two devices to connect
5. Select Auto-Drive (1) And Choose Start


## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.