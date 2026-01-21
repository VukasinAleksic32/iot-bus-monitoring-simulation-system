import json
import paho.mqtt.client as mqtt
import config
import database

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    print("Received:", data)
    database.save_bus(data)

client = mqtt.Client()
client.on_message = on_message

def start():
    client.connect(config.BROKER, config.PORT, 60)
    client.subscribe("bus/+/people")
    client.loop_start()
