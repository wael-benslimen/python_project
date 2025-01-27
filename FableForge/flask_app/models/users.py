from flask_app.config.mySQLConnection import connectToMySQL
from flask_app.models.charcters import Charcter
from flask import flash
from flask_app import DB




class User:
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.adminstration = 'user'
        self.messages = []
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.charcter_id = data['charcter_id']
        
        
    @classmethod    
    def create(cls, data):
        query = 'insert into users(id, username, email, password, adminstration, charcter_id) values(%(id)s, %(username)s, %(email)s, %(adminstration)s, %(charcter_id)s )'
        return connectToMySQL(DB).query_db(query, data)
    
    
    @classmethod
    def get_all(cls):
        query = 'select * from users'
        result = connectToMySQL(DB).query_db(query)
        arr = []
        for item in result:
            arr.append(cls(item))
        return arr
    
    @classmethod
    def get_one_id(cls, data):
        query = 'select * from users where id = %(id)s)'
        result = connectToMySQL(DB).query_db(query, data)
        if result:
            return cls(result[0])
        else:
            return False
        
    @classmethod
    def update(cls, data):
        query = 'update users set username = %(username)s, email = %(email)s, password = %(password)s where id = %(id)s'
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def ban(cls, data):
        query = 'update users set adminstration = "ban" where id = %(id)s '
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def unban_demote(cls, data):
        query = 'update users set adminstration = "user" where id = %(id)s'
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def promote(cls, data):
        query = 'update users set adminstration = "mod" where id = %(id)s'
        return connectToMySQL(DB).query_db(query, data)
    
    @staticmethod
    def validate_user(data):
        is_valid = True
        if data['username'] == '':
            is_valid = False
            flash('username should not be empty', 'username_eror')
        if 