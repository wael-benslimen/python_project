from flask import render_template,session,redirect,request,flash
from flask_app import app
from flask_app.models.users import User
from flask_bcrypt import Bcrypt 
bcrypt=Bcrypt(app)

@app.route('/login')
def index():
    return render_template("index.html")



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
    return redirect('/')

@app.route("/user/login", methods = ['POST'])
def login():
    user = User.get_by_email({"email": request.form['email']})
    if not user:
        flash("Ivalid credentials!", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form["password"]):
        flash("Invalid credentials!", "login")
        return redirect('/')
    session["user_id"] = user.id
    return redirect("/dashboard")

@app.route('/logout', methods = ['post'])
def logout():
    session.clear()
    return redirect('/')


@app.route('/edit/form')
def display_edit_form() :
    if 'user_id' not in session :
        return redirect('/')
    user = User.get_one_id({'id':session['user_id']})
    print("Session user_id:", session['user_id'])
    return render_template('edit_profile.html',user=user)


@app.route('/edit/user',methods=['POST'])
def edit_user() :
    if 'user_id' not in session :
        return redirect('/')
    if User.validate_user(request.form) :
        hached_pw = bcrypt.generate_password_hash(request.form["password"])
        data = {
            **request.form,
            "password": hached_pw,
            'id':session['user_id']
        }
        print(22222222222222222222222222222222222222222222222)
        User.update(data)
        print("*"*100)
        print(data)
        return redirect('/dashboard')
    return redirect('/edit/form')