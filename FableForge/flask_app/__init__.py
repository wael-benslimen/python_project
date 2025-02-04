from flask import Flask
from flask_socketio import SocketIO, join_room, leave_room, send
app = Flask(__name__)
app.secret_key = "secret_key"
DB  = "fable_forge_schema"
socketio = SocketIO(app)

