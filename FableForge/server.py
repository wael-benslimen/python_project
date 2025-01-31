from flask_app import app,socketio
from flask_app.controllers import user_controller, dashboard
from flask_cors import CORS
cors = CORS(app, resources={r"/*": {"origins": "http://localhost:5000"}})
def create_app():
    app.config['SECRET_KEY'] = 'secret!'
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)