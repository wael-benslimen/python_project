from flask_app import app
from flask_app.controllers import user_controller,landing_page_controller, dashboard,freinds_controller

if __name__ == "__main__":
    app.run(debug=True, port= 5001)