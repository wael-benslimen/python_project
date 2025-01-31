from flask_app import socketio
from flask_socketio import send
from flask import session,request
@socketio.on('message')
def handle_message(msg):
    print('Message: ' + msg)
    send(msg, broadcast=True)
@socketio.on("typing")
def send(msg):
    print(f"{msg['username']} is typing...")
    send(f"{msg['username']} is typing...", room=msg['room'], broadcast=True)