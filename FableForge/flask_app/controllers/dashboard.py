from flask import render_template, session, redirect, request, flash,jsonify
from flask_app import app
from flask_app.models.users import User
from flask_app.models.tasks import Task
from flask_app.models.friends import Friend
from flask_app.models.messages import Message
import schedule
import time
import threading
import math


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/register')
    user = User.get_one_id({'id': session['user_id']})
    all_quests = Task.get_user_tasks({'user_id': session['user_id']})
    if user:
        latest_messages = Message.get_latest()
        print("*"*100)
        print(latest_messages)
        if user.adminstration == "adminstration":
            latest_users = User.get_latest_users_count()
            active_users = User.get_active_users()
            users_count = User.get_users_count()
            return render_template('dashboard.html', user=user, all_quests=all_quests,latest_users=latest_users,active_users=active_users,users_count=users_count,latest_messages=latest_messages)
        else:
            return render_template('dashboard.html', user=user, all_quests=all_quests,latest_messages=latest_messages)
    else:
        flash("Invalid user_id", "error")
        return redirect('/register')
@app.route("/users/<int:p>")
def get_users(p):
    users:list[User] = User.get_users_by_amount({"limit": 10, "offset": p})
    return jsonify({"users": [user.to_dict() for user in users],"page":p}), 200

@app.route("/latest-users/<int:p>")
def get_latest_users(p):
    users:list[User] = User.get_latest_users({"limit": 10, "offset": p})
    return jsonify({"users": [user.to_dict() for user in users],"page":p}), 200
@app.route('/admin_dashboard')
def admin_dashboard() :
    if 'user_id' in session:
        user = User.get_one_id({'id': session['user_id']})
        all_quests = Task.get_user_tasks({'user_id': session['user_id']})
        if user:
            if user.adminstration == "adminstration":
                latest_users_count:int = User.get_latest_users_count()
                active_users:int = User.get_active_users()
                latest_users = [u.to_dict() for u in User.get_latest_users({"limit": 10, "offset": 0}) if isinstance(u, User)]
                users_count:int = User.get_users_count()
                users:list[User] = [u.to_dict() for u in User.get_users_by_amount({"limit":10, "offset":0}) if isinstance(u, User)]
                users_pages_count:int = math.ceil(User.get_users_count()/10)
                latest_users_pages_count:int = math.ceil(latest_users_count/10)
                users_grouped_by_month = User.get_users_grouped_by_month()
                progress = User.get_latest_users_count() - User.get_latest_users_count_compared()
                return render_template(
                    'admin_dashboard.html', 
                    user=user, 
                    all_quests=all_quests,
                    latest_users_count=latest_users_count,
                    latest_users=latest_users,
                    active_users=active_users,
                    users_count=users_count,
                    users=users,
                    pages_count=users_pages_count,
                    latest_users_pages_count=latest_users_pages_count,
                    users_grouped_by_month=users_grouped_by_month,
                    page=1,
                    progress=progress/len(users)
                )
            else:
                return redirect("/dashboard")
        else:
            flash("Invalid user_id", "error")
            return redirect('/register')
    else:
        flash("Invalid user_id", "error")
        return redirect('/register')
@app.route('/create_quest', methods=['POST'])
def create_quest():
    if Task.validate_task(request.form):
        data = {
            **request.form,
            'user_id': session['user_id']
        }
        print(session)
        Task.create(data)
        print("*" * 100)
        return redirect('/dashboard')
    return redirect('/dashboard')
@app.route("/user/<int:id>")
def user_by_id(id):
    if "user_id" in session:
        found_user = User.get_one_id({"id":session["user_id"]})
        if found_user:
            user = User.get_one_id({"id":id})
            return render_template("profile.html",user=user.to_dict())
        else:
            return redirect("/")
    else:
        return redirect("/")
@app.route('/cancle/<int:id>', methods=['POST'])
def delete_quest(id):
    Task.delete({'id': id})
    return redirect('/dashboard')

@app.route('/finished/<int:id>', methods=['POST'])
def finished_quest(id):
    user = User.get_one_id({'id': session['user_id']}) 
    task = Task.select_id({"id":id})  
    print('8'*100)
    print(task['task_difficulty'])
    if user.exp < 95:
        if task["task_difficulty"] == 1:
            Task.lvl_up_easy({'id': session['user_id']})
            Task.delete({'id': id})
        elif task["task_difficulty"] == 2:
            Task.lvl_up_medium({'id': session['user_id']})
            Task.delete({'id': id})
        elif task["task_difficulty"] == 3:
            Task.lvl_up_hard({'id': session['user_id']})
            Task.delete({'id': id})

            
    else:
        Task.reset_exp({'id': session['user_id']})
        Task.lvl_plus({'id': session['user_id']})
    return redirect('/dashboard')


@app.route('/lvl_up', methods=['POST'])
def lvl_up():
    data = {
        **request.form,
        'id': session['user_id']
    }
    User.add_equipments(data)
    Task.reset_exp({'id': session['user_id']})
    Task.lvl_plus({'id': session['user_id']})
    return redirect('/dashboard')

@app.route('/inv_items', methods=['POST'])
def inv_item():
    user = User.get_one_id({'id': session['user_id']})
    data = {
        'id': session['user_id']
    }
    if request.form['item'] == 'hp':
        User.add_HP(data)
        user.inv_items = user.inv_items.replace('hp', '')
    if request.form['item'] == 'apple':
        Task.lvl_plus(data)
        user.inv_items = user.inv_items.replace('apple', '')
    if request.form['item'] == 'bean':
        Task.lvl_up_hard(data)
        user.inv_items = user.inv_items.replace('bean', '')
    if request.form['item'] == 'revive':
        User.max_HP(data)
        Task.reset_exp(data)
        user.inv_items = user.inv_items.replace('revive', '')
        print('*'*50)
    print(user.inv_items)
    User.update_inv({'id': session['user_id'], 'inv_items': user.inv_items})
    return redirect('/dashboard')

@app.route('/max_lvl', methods=['POST'])
def max_lvl():
    data = {
        **request.form,
        'id': session['user_id']
    }
    print('*'*100)
    print(data)
    User.add_pet(data)
    Task.reset_exp(data)
    Task.lvl_plus(data)
    return redirect('/dashboard')

@app.route('/restart', methods=['POST'])
def restart():
    data = {
        'id': session['user_id']
    }
    User.max_HP(data)
    User.reset_inv(data)
    Task.reset_exp(data)
    User.reset_lvl(data)
    User.reset_pet(data)
    User.reset_equipment(data)
    return redirect('/dashboard')

def check_tasks():
    print("*"*100)
    print("Checking tasks")
    users = User.get_all()
    for user in users:
        user_tasks = Task.get_user_tasks({'user_id': user.id})
        if user_tasks:
            User.depleat_HP({'id': user.id})

def run_scheduler():
    schedule.every().day.at("00:00").do(check_tasks)
    while True:
        schedule.run_pending()
        time.sleep(1)

scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.daemon = True
scheduler_thread.start()
