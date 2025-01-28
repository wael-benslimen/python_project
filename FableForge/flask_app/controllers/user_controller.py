from flask import render_template,session,redirect,request,flash
from flask_app import app
from flask_app.models.users import User
from flask_bcrypt import Bcrypt 
bcrypt=Bcrypt(app)

@app.route('/')
def index():
    return render_template("login.html")

@app.route("/create/new", methods = ["post"])
def register():
    if User.validate_user(request.form):
        hached_pw = bcrypt.generate_password_hash(request.form["password"])
        data = {
            **request.form,
            "password": hached_pw
        }
        user_id = User.register(data)
        session["user_id"] = user_id
        return redirect('/dashboard')
    return redirect('/signup')

@app.route("/login", methods = ['POST'])
def login():
    user = User.get_by_email({"email": request.form['email']})
    if not user:
        flash("Ivalid credentials!", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form["password"]):
        flash("Invalid credentials!", "login")
        return redirect('/')
    session["uer_id"] = user.id
    return redirect("/dashboard")

@app.route('/logout', methods = ['post'])
def logout():
    session.clear()
    return redirect('/')
