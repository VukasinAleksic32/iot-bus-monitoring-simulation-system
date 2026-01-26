import json
import time
import paho.mqtt.client as mqtt
from bus import Bus
import config

# MQTT client setup
client = mqtt.Client()
client.connect(config.BROKER, config.PORT, 60)
client.loop_start()

# Initialize buses
buses = [Bus(i) for i in range(config.BUS_COUNT)]

# Simulation loop
try:
    while True:
        for bus in buses:
            data = bus.step()
            topic = f"bus/{bus.id}/people"
            client.publish(topic, json.dumps(data))

        time.sleep(config.PUBLISH_INTERVAL)

except KeyboardInterrupt:
    client.loop_stop
    client.disconnect()