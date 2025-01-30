from flask import render_template, session, redirect, request, flash
from flask_app import app
from flask_app.models.users import User
from flask_app.models.tasks import Task
from flask_app.models.friends import Friend
from flask_app.models.messages import Message

c_quest = 0
f_quest = 0

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_one_id({'id': session['user_id']})
    print('*'*100)
    print(user)
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

@app.route('/cancle/<int:id>', methods = ['POST'])
def delete_quest(id):
    Task.delete({'id': id})
    return redirect('/dashboard')

@app.route('/finished/<int:id>', methods = ['POST'])
def finished_quest(id):
    user = User.get_one_id({'id': session['user_id']})
    if user.exp < 100:
        Task.lvl_up({'id': session['user_id']})
        Task.delete({'id': id})
    else:
        Task.reset_exp({'id': session['user_id']})
        Task.lvl_plus({'id': session['user_id']})
    return redirect('/dashboard')

@app.route('/lvl_up', methods=['POST'])
def lvl_up():

    return redirect('/dashboard')