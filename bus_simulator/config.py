import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from shared.config import BROKER, PORT

# Simulation settings
BUS_COUNT = 12
PUBLISH_INTERVAL = 1.0