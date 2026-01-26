from flask import Flask, jsonify
import mqtt_client
import database

app = Flask(__name__)
mqtt_client.start()

# API routes
@app.get("/api/buses")
def buses():
    return jsonify(database.get_all_buses())
