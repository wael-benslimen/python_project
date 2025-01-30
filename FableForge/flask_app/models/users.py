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
        self.adminstration = 'user'
        self.char_lvl= 1
        self.location = ""
        self.about_me = ""
        self.interests = ""
        self.exp = data['exp']
        self.HP= 4
        self.image = ""
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
        
    @classmethod    
    def register(cls, data):
        query = "INSERT INTO users(username, email, password) VALUES (%(username)s, %(email)s, %(password)s) ;"
        return connectToMySQL(DB).query_db(query, data)
    
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users ;"
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
    def get_one_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s ;"
        result = connectToMySQL(DB).query_db(query, data)
        print('*'*100)
        print(result)
        if result:
            return cls(result[0])
        else:
            return False
        
    @classmethod
    def update(cls, data):
        query = "UPDATE users SET username = %(username)s, email = %(email)s, password = %(password)s,location=%(location)s,about_me=%(about_me)s,interests=%(interests)s where id = %(id)s ;"
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def ban(cls, data):
        query = 'update users set adminstration = "ban" where id = %(id)s '
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def unban_demote(cls, data):
        query = 'update users set adminstration = "user" where id = %(id)s'
        return connectToMySQL(DB).query_db(query, data)
    
    
    @staticmethod
    def validate_user(data):
        is_valid = True
        if data['username'] == '':
            is_valid = False
            flash('username should not be empty', 'username')
        if not EMAIL_REGEX.match(data['email']) :
            is_valid=False
            flash("Email not valid,try again","email")
        if len(data['password']) < 8 :
            is_valid= False
            flash("Password must contain at least 8 characters","password")
        if data['password'] != data['confirm-password'] :
            is_valid=False 
            flash("Passwords must match","confirm-password")
        return is_valid