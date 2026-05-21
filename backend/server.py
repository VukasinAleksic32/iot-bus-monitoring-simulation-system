from flask import Flask
from flask_socketio import emit
import database
from extensions import socketio

app = Flask(__name__)

# Send current state to newly connected client
@socketio.on("connect")
def on_connect():
    emit("initial_state", database.get_all_buses())