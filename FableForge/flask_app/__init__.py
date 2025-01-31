from flask_socketio import SocketIO, send
from flask import Flask
app = Flask(__name__)
app.secret_key = "secret_key"
socketio = SocketIO(app)
DB  = "fable_forge_schema"
