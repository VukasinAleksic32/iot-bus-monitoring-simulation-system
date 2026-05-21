import json
import time
import paho.mqtt.client as mqtt
from bus import Bus
import config

# MQTT client setup
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(config.BROKER, config.PORT, 60)
client.loop_start()

print("Bus simulator started. Press Ctrl+C to stop.")

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
    print("\nStopping simulator...")
finally:
    client.loop_stop()
    client.disconnect()
    print("MQTT disconnected.")