from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.users import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "username": request.form['username'],
        "email": request.form['email'],
        "password": pw_hash
    }
    user_id = User.register(data)
    session['user_id'] = user_id
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    data = { "email": request.form["email"] }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password", "login")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_one_id({'id': session['user_id']})
    return render_template('profile.html', user=user)

@app.route('/edit/form')
def edit_form():
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_one_id({'id': session['user_id']})
    return render_template('edit_profile.html', user=user)

@app.route('/edit', methods=['POST'])
def edit():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": session['user_id'],
        "username": request.form['username'],
        "email": request.form['email'],
        "location": request.form['location'],
        "about_me": request.form['about_me'],
        "interests": request.form['interests']
    }
    User.update(data)
    return redirect('/profile')

@app.route('/offline')
def offline():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": session['user_id'],
        "is_active": 0
    }
    User.update(data)
    return redirect('/dashboard')
