from flask import render_template, session, redirect, request, flash
from flask_app import app
from flask_app.models.users import User
from flask_app.models.tasks import Task
from flask_app.models.friends import Friend
from flask_app.models.messages import Message

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_one_id({'id': session['user_id']})
    all_quests = Task.get_user_tasks({'user_id': session['user_id']})
    return render_template('dashboard.html', user=user, all_quests=all_quests)

@app.route('/create_quest', methods=['POST'])
def create_quest():
    if Task.validate_task(request.form):
        data = {
            **request.form,
            'user_id': session['user_id']
        }
        Task.create(data)
        return redirect('/dashboard')
    return redirect('/dashboard')




