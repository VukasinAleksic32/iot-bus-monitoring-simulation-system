from server import app
from extensions import socketio
import mqtt_service
import config

socketio.init_app(app)
mqtt_service.start()

if __name__ == "__main__":

    # Start Flask server
    socketio.run(app, host=config.API_HOST, port=config.API_PORT, debug=False)