from flask_app.config.mySQLConnection import connectToMySQL
from flask import flash
from flask_app import DB
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.adminstration = data.get('adminstration', 'user')
        self.char_lvl = data.get('char_lvl', 1)
        self.location = data.get('location', "")
        self.about_me = data.get('about_me', "")
        self.interests = data.get('interests', "")
        self.exp = data['exp']
        self.HP = data.get('HP', 4)
        self.type = data.get('type')
        self.equipments = data.get('equipments', "")
        self.image = data.get('image', "")
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.is_friend=False
        self.views = data.get('views', 0)
        self.is_active = data.get('is_active', 0)
        
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "is_active": self.is_active or 0,
            "adminstration": self.adminstration,
            "char_lvl": self.char_lvl,
            "location": self.location,
            "about_me": self.about_me,
            "interests": self.interests,
            "exp": self.exp,
            "HP": self.HP,
            "type": self.type,
            "equipments": self.equipments,
            "image": self.image or "",
            "views": self.views or 0,
        }
    @classmethod    
    def register(cls, data):
        query = "INSERT INTO users(username, email, password) VALUES (%(username)s, %(email)s, %(password)s);"
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        result = connectToMySQL(DB).query_db(query)
        all_users = []
        for row in result:
            all_users.append(cls(row))
        return all_users
    
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DB).query_db(query, data)
        if result:
            return cls(result[0])
        return False
    
    @classmethod
    def select_char(cls, data):
        query = """UPDATE users SET type = %(type)s WHERE id = %(id)s;"""
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def choose_inter(cls, data):
        query = """UPDATE users SET interests = %(interests)s WHERE id = %(id)s;"""
        return connectToMySQL(DB).query_db(query, data)
        
    @classmethod
    def get_one_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(DB).query_db(query, data)
        if result:
            return cls(result[0])
        else:
            return False
        
    @classmethod
    def update(cls, data):
        query = """UPDATE users SET username = %(username)s, email = %(email)s, password = %(password)s,
                location = %(location)s, interests = %(interests)s WHERE id = %(id)s;"""
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def ban(cls, data):
        query = 'UPDATE users SET adminstration = "ban" WHERE id = %(id)s;'
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def unban_demote(cls, data):
        query = 'UPDATE users SET adminstration = "user" WHERE id = %(id)s;'
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def add_equipments(cls, data):
        query = 'UPDATE users SET equipments = equipments + %(equipment)s WHERE id = %(id)s;'
        return connectToMySQL(DB).query_db(query, data)


    
    @classmethod
    def not_friends_users(cls, logged_in_user_id):
        query = """
        SELECT users.* 
        FROM users
        LEFT JOIN friends AS friendships_1 ON users.id = friendships_1.friend_id AND friendships_1.user_id = %(logged_in_user_id)s
        LEFT JOIN friends AS friendships_2 ON users.id = friendships_2.user_id AND friendships_2.friend_id = %(logged_in_user_id)s
        WHERE users.id != %(logged_in_user_id)s
        AND (friendships_1.friend_id IS NULL AND friendships_2.user_id IS NULL);
        """
        data = {'logged_in_user_id': logged_in_user_id}
        results = connectToMySQL(DB).query_db(query, data)
        users_not_friends = []
        for row in results:
            user_not_friend = cls(row)
            users_not_friends.append(user_not_friend)
        return users_not_friends

    @classmethod
    def find_users(cls,data) :
        query="""
        SELECT username
        FROM users 
        LEFT JOIN friends AS friendships  ON users.id = friendships.friend_id AND friendships.user_id = 1
        LEFT JOIN friends f2 ON users.id = f2.user_id AND f2.friend_id = 1
        WHERE users.id != 1 AND friendships.friend_id IS NULL AND f2.user_id IS NULL AND  username LIKE %(username)s ;
        """
        data["username"] = f"{data['username']}%"
        result = connectToMySQL(DB).query_db(query, data)
        return [row['username'] for row in result]
    
    @classmethod
    def update_bio(cls, data):
        query = "UPDATE users SET about_me = %(about_me)s WHERE id = %(user_id)s"
        return connectToMySQL(DB).query_db(query, data)
        

        
    @staticmethod
    def validate_user(data):
        is_valid = True
        if data['username'] == '':
            is_valid = False
            flash('Username should not be empty', 'username')
        if not EMAIL_REGEX.match(data['email']):
            is_valid = False
            flash("Email not valid, try again", "email")
        if len(data['password']) < 8:
            is_valid = False
            flash("Password must contain at least 8 characters", "password")
        if data['password'] != data['confirm-password']:
            is_valid = False
            flash("Passwords must match", "confirm-password")
        return is_valid
    @classmethod
    def get_users_username(cls, data):
        query = """
            SELECT * 
            FROM users 
            LEFT JOIN friends AS friendships ON users.id = friendships.friend_id AND friendships.user_id = 1
            LEFT JOIN friends f2 ON users.id = f2.user_id AND f2.friend_id = 1
            WHERE users.id != 1 AND friendships.friend_id IS NULL AND f2.user_id IS NULL AND username LIKE %(username)s;
        """
        results = connectToMySQL(DB).query_db(query, data)
        return [cls(u).to_dict() for u in results if u]