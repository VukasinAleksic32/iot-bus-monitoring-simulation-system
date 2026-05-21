from flask_socketio import SocketIO

# Allow frontend to connect via WebSocket
socketio = SocketIO(cors_allowed_origins="*")