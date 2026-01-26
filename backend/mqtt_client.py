import json
import paho.mqtt.client as mqtt
import config
import database

# Message handler
def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    print("Received:", data)
    database.save_bus(data)

# MQQT client setup
client = mqtt.Client()
client.on_message = on_message

# Start client
def start():
    client.connect(config.BROKER, config.PORT, 60)
    client.subscribe("bus/+/people")
    client.loop_start()
