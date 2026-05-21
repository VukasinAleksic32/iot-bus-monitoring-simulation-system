import json
import paho.mqtt.client as mqtt
import config
import database
from extensions import socketio

# Message handler
def on_message(client, userdata, message):
    data = json.loads(message.payload.decode())
    database.save_bus(data)
    socketio.emit("bus_update", data)

# MQTT client setup
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message

# Start client
def start():
    client.connect(config.BROKER, config.PORT, 60)
    client.subscribe(config.TOPIC)
    client.loop_start()