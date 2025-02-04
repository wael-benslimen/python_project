from flask_app import app
from flask_app.controllers import user_controller,landing_page_controller, dashboard,freinds_controller
from flask_socketio import SocketIO, send
from flask_cors import CORS
from flask_app import socketio
from flask_socketio import send
from flask import session,request

# Initialize SocketIO and CORS
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

cors = CORS(app, resources={r"/*": {"origins": "http://localhost:5000"}})
def create_app():
    app.config['SECRET_KEY'] = 'secret!'
    return app


@socketio.on('message')
def handle_message(msg):
    print('Message: ' + msg)
    send(msg, broadcast=True)
@socketio.on("typing")
def send(msg):
    print(f"{msg['username']} is typing...")
    send(f"{msg['username']} is typing...", room=msg['room'], broadcast=True)



if __name__ == "__main__":
    app = create_app()
    socketio.run(app, debug=True, port=5000)