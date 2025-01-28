from flask_app.config.mySQLConnection import connectToMySQL
from flask_app.models.charcters import Charcter
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
        self.HP= 4
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.charcter_id = data['charcter_id']
        
        
    @classmethod    
    def create(cls, data):
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
    def get_one_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s) ;"
        result = connectToMySQL(DB).query_db(query, data)
        if result:
            return cls(result[0])
        else:
            return False
        
    @classmethod
    def update(cls, data):
        query = "UPDATE users set username = %(username)s, email = %(email)s, password = %(password)s where id = %(id)s ;"
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
            flash('username should not be empty', 'username_eror')
        if not EMAIL_REGEX.match(data['email']) :
            is_valid=False
            flash("Email not valid,try again","email_validation")
        if len(data['password']) < 3 :
            is_valid= False
            flash("Password must contain at least 5 characters","password_validation")
        if data['password'] != data['password_confimation'] :
            is_valid=False 
            flash("Passwords must match","password_confirmation")
        return is_valid