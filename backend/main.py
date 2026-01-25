from flask import Flask
from flask_cors import CORS
from server import app as flask_app
import config

CORS(flask_app)
if __name__ == "__main__":
    flask_app.run(
        host=config.API_HOST,
        port=config.API_PORT,
        debug=False
    )
