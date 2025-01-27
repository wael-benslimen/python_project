from flask_app.config.mySQLConnection import connectToMySQL
from flask_app import DB


class Charcter:
    def __init__(self, data):
        self.id = data['id']
        self.type = data['class']
        self.lvl = 1
        self.hp = 100
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def create(cls, data):
        query = 'insert into charcters(type) values (%(class)s) '
        return connectToMySQL(DB).query_db(query, data)
        
    @classmethod
    def get_one(cls, data):
        query = 'select * from charcters where id = %(id)s '
        result = connectToMySQL(DB).query_db(query, data)
        if result:
            return cls(result[0])
        else:
            return False