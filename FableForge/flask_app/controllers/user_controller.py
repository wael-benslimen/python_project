from flask import render_template,session,redirect,request,flash
from flask_app import app
from flask_app.models.users import User
from flask_bcrypt import Bcrypt 
bcrypt=app(Bcrypt)

@app.route('/')
def index() :
    return render_template("/index.html")
