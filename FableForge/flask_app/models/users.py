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
        self.is_active = data.get('is_active', 0)
        self.inv_items = data.get('inv_items', 'applehprevivebean')
    @classmethod    
    def register(cls, data):
        query = "INSERT INTO users(username, email, password) VALUES (%(username)s, %(email)s, %(password)s);"
        new_id = connectToMySQL(DB).query_db(query, data)
        new_user = cls.get_one_id({'id': new_id})
        return new_user
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        result = connectToMySQL(DB).query_db(query)
        all_users = []
        for row in result:
            all_users.append(cls(row))
        return all_users
    
    @classmethod
    def get_users_by_amount(cls,data):
        query = "SELECT * FROM users LIMIT %(limit)s OFFSET %(offset)s;"
        result = connectToMySQL(DB).query_db(query, data)
        all_users = []
        for row in result:
            all_users.append(cls(row))
        return all_users
    @classmethod
    def get_latest_users_by_amount(cls,data):
        query = "SELECT * FROM users ORDER BY created_at DESC LIMIT %(limit)s OFFSET %(offset)s;"
        result = connectToMySQL(DB).query_db(query, data)
        all_users = []
        for row in result:
            all_users.append(cls(row))
        return all_users
    
    @classmethod
    def get_latest_users_count(cls):
        query = "SELECT COUNT(*) FROM users WHERE created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY);"
        result = connectToMySQL(DB).query_db(query)
        return result[0]
    
    @classmethod
    def get_active_users(cls):
        query = "SELECT COUNT(*) FROM users WHERE adminstration = 'user' AND is_active = 1;"
        result = connectToMySQL(DB).query_db(query)
        return result[0]
    
    @classmethod
    def get_users_count(cls):
        query = "SELECT COUNT(*) FROM users;"
        result = connectToMySQL(DB).query_db(query)
        return result[0]
    
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DB).query_db(query, data)
        if result:
            return cls(result[0])
        return False
    
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
                location = %(location)s, about_me = %(about_me)s, interests = %(interests)s WHERE id = %(id)s;"""
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
        query = 'UPDATE users SET equipments = %(equipment)s WHERE id = %(id)s;'
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def depleat_HP(cls, data):
        query = 'UPDATE users SET HP = HP - 25 WHERE id = %(id)s;'
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def add_HP(cls, data):
        query = 'UPDATE users SET HP = hp + 25 WHERE id = %(id)s;'
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def max_HP(cls, data):
        query = 'UPDATE users SET HP = 100 WHERE id = %(id)s;'
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def update_inv(cls, data):
        query = 'UPDATE users SET inv_items = %(inv_items)s WHERE id = %(id)s;'
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