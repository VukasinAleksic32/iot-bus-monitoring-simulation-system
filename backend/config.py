import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from shared.config import BROKER, PORT

# Flask server configuration
API_HOST = "0.0.0.0"
API_PORT = 5000

# Topic structure
TOPIC = "bus/+/people"