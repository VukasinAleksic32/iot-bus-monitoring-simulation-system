import json
import time
import paho.mqtt.client as mqtt
from bus import Bus
import config

client = mqtt.Client()
client.connect(config.BROKER, config.PORT, 60)

buses = [Bus(i) for i in range(config.BUS_COUNT)]

while True:
    for bus in buses:
        data = bus.step()
        topic = f"bus/{bus.id}/people"
        client.publish(topic, json.dumps(data))
    time.sleep(config.PUBLISH_INTERVAL)
