from flask import render_template,session,redirect,request,jsonify,flash
from flask_app import app
from flask_app.models.friends import Friend 
from flask_app.models.users import User




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
    all_friends=Friend.get_friends_by_user(logged_in_user)
    return render_template('user_profile_friend.html',all_friends=all_friends,user=user)


@app.route('/friend/<int:friend_id>')
def view_friend(friend_id):
    friend = Friend.get_one_friend(friend_id)
    if friend:
        return render_template('view_one_friend.html', friend=friend)
    else:
        flash("Friend not found!")
        return redirect('/dashboard') 

@app.route("/friend/by-name/<username>")
def get_friends(username):
    print(username)
    friends =User.get_users_username({"username":username})
    return jsonify({"friends":friends})

@app.route('/remove/friend/',methods=['POST'])
def remove_friend() :
    user_id=session['user_id']
    friend_id=request.form['friend_id']
    Friend.remove_friend(user_id, friend_id)
    return redirect('/profile/friends')