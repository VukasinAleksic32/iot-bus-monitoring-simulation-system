from flask import Flask
from flask_cors import CORS
from server import app as flask_app
import config
import os

db_path = "backend/buses.db"

# Reset DB on each simulation start
if os.path.exists(db_path):
    os.remove(db_path)
    print("Database reset: buses.db deleted.")
else:
    print("Database file not found, creating a new one.")

CORS(flask_app)
if __name__ == "__main__":
    flask_app.run(
        host=config.API_HOST,
        port=config.API_PORT,
        debug=False
    )
