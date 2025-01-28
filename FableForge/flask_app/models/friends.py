from flask_app.config.mySQLConnection import connectToMySQL
from flask_app import DB


class Friend :
    def __init__(self,data) :
        self.id=data['id']
        self.user_id=data['user_id']
        self.friend_id=data['friend_id']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        
        
        
    @classmethod
    def create(cls,data) :
        query="INSERT INTO friends (user_id,friend_id) VALUES (%(user_id)s,%(friend_id)s) ;"
        return connectToMySQL(DB).query_db(query,data)
    
    
    @classmethod
    def get_one(cls,data) :
        query="SELECT * FROM friends WHERE id=%(id)s ;"
        result = connectToMySQL(DB).query_db(query, data)
        if result:
            return cls(result[0])
        else:
            return False
    
    @classmethod
    def get_all(cls) :
        query="SELECT * FROM friends ;"
        results = connectToMySQL(DB).query_db(query)
        all_friends=[]
        for row in results :
            friend=cls(row)
            all_friends.append(friend)
        return all_friends
    

    
    @classmethod
    def delete(cls,data) :
        query="DELETE FROM friends WHERE id=%(id)s ;"
        return connectToMySQL(DB).query_db(query,data)