#!/bin/bash

echo "================================"
echo "       Starting IoT Project"
echo "================================"

# ---------------------------------
# Check if Mosquitto is installed
# ---------------------------------
if ! command -v mosquitto >/dev/null 2>&1; then
    echo "ERROR: Mosquitto MQTT broker is not installed!"
    echo "Install with:"
    echo "  sudo apt install mosquitto mosquitto-clients"
    exit 1
fi

# ---------------------------------
# Check if Mosquitto is already running
# ---------------------------------
if pgrep -x "mosquitto" >/dev/null; then
    echo "Mosquitto is already running. Skipping start."
    MOSQUITTO_RUNNING=true
else
    MOSQUITTO_RUNNING=false
fi

# ---------------------------------
# Check if port 1883 is in use
# ---------------------------------
if ss -tulnp | grep ":1883" >/dev/null; then
    echo "Port 1883 is already in use. Assuming MQTT broker is running."
    MOSQUITTO_RUNNING=true
fi

# ---------------------------------
# Start Mosquitto MQTT Broker
# ---------------------------------
if [ "$MOSQUITTO_RUNNING" = false ]; then
    echo "Starting Mosquitto broker..."
    sudo systemctl start mosquitto
    sleep 2
fi

echo "Mosquitto check complete."

# ---------------------------------
# Create virtual environment if missing
# ---------------------------------
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Creating .venv..."
    python3 -m venv .venv
else
    echo "Virtual environment found."
fi

# ---------------------------------
# Activate virtual environment
# ---------------------------------
echo "Activating virtual environment..."
source .venv/bin/activate

# ---------------------------------
# Install dependencies
# ---------------------------------
echo "Installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt

# ---------------------------------
# Start backend server
# ---------------------------------
echo "Starting backend (Flask)..."
gnome-terminal -- bash -c "source $(pwd)/.venv/bin/activate; python3 backend/main.py; exec bash"

# ---------------------------------
# Start bus simulator
# ---------------------------------
echo "Starting bus simulator..."
gnome-terminal -- bash -c "source $(pwd)/.venv/bin/activate; python3 bus_simulator/main.py; exec bash"

# ---------------------------------
# Open frontend
# ---------------------------------
echo "Opening frontend..."
xdg-open "frontend/index.html" >/dev/null 2>&1 &

echo "================================"
echo " Project started successfully!"
echo "================================"
