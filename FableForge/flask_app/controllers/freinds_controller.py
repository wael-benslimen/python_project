from flask import render_template,session,redirect,request,jsonify,flash
from flask_app import app
from flask_app.models.friends import Friend 
from flask_app.models.users import User
from flask_app.models.tasks import Task




@app.route('/friends/suggestions')
def friends_suggestions():
    if 'user_id' not in session:
        return redirect('/login')
    logged_in_user_id = session['user_id']
    not_friends = User.not_friends_users(logged_in_user_id)
    print('*'*100)
    return render_template('friends_suggestions.html', not_friends=not_friends)




@app.route('/add_friend',methods=['POST'])
def add_friend() :
    print('A'* 100)
    user_id = session['user_id']
    not_friend_id = request.form['friend_id']
    if not_friend_id != user_id :
        data = {
        'user_id': user_id,
        'friend_id': not_friend_id
        }
        Friend.create(data)
        print('A'* 100)
        print('user_id :',user_id ,'and','not_friend :',not_friend_id)
        return redirect('/friends/suggestions')
    else : 
        flash("Action failed!")
        return redirect('/friends/suggestions')



@app.route('/profile/friends')
def all_friends():
    logged_in_user=session['user_id']
    user = User.get_one_id({'id':logged_in_user})
    all_quests = Task.get_user_tasks({'user_id':logged_in_user})
    all_friends=Friend.get_friends_by_user(logged_in_user)
    return render_template('user_profile_friend.html',all_friends=all_friends,user=user,all_quests=all_quests)


@app.route('/friend/<int:friend_id>')
def view_friend(friend_id):
    friend = Friend.get_one_friend(friend_id)
    all_quests = Task.get_user_tasks({'user_id':friend_id})
    if friend:
        return render_template('view_one_friend.html', friend=friend,all_quests=all_quests)
    else:
        flash("Friend not found!")
        return redirect('/dashboard') 

@app.route("/friend/by-name/<username>")
def get_friends(username):
    friends =Friend.get_friends_by_user(session['user_id'])
    found_friends = []
    for friend in friends:
        if friend['username'].lower().startswith(username.lower()):
            found_friends.append(friend)
    return jsonify({"friends":found_friends})


@app.route("/friend/by-interests/<interests>")
def get_users_by_interests(interests):
    users =User.not_friends_users(session['user_id'])
    not_friends = []
    for user in users:
        if user and user.interests and user.interests.lower().startswith(interests.lower()):
            not_friends.append(user.to_dict())
    return jsonify({"users":not_friends})

@app.route('/remove/friend/',methods=['POST'])
def remove_friend() :
    user_id=session['user_id']
    friend_id=request.form['friend_id']
    Friend.remove_friend(user_id, friend_id)
    return redirect('/profile/friends')