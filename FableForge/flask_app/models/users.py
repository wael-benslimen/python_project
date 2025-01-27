from flask_app.config.mySQLConnection import connectToMySQL
from flask_app.models.charcter import Charcter
from flask_app import DB




class User:
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.adminstration = data['adminstration']
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
    
    