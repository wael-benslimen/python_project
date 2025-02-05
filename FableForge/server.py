from flask_app import app
from flask_app.controllers import user_controller,landing_page_controller, dashboard,freinds_controller
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS
from flask_app import socketio
from flask import session
from flask_app.models.messages import Message
# Initialize SocketIO and CORS
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

cors = CORS(app, resources={r"/*": {"origins": "http://localhost:5000"}})
def create_app():
    app.config['SECRET_KEY'] = 'secret!'
    return app

@socketio.on('send-message')
def handle_chat_message(msg):
    print('Message: ' + msg["message"])
    print(msg["user_id"])
    Message.create(msg)
    emit('receive-message', {"message":msg["message"],"username":msg['username']}, broadcast=True)

@socketio.on('typing')
def handle_typing(data):
    print(f"{data['username']} is typing...")
    emit('typing', data, broadcast=True)

if __name__ == "__main__":
    app = create_app()
    socketio.run(app, debug=True, port=5000)