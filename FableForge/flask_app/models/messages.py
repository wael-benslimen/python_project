from flask_app.config.mySQLConnection import connectToMySQL
from flask_app import DB 


class Message :
    def __init__(self,data) :
        self.id=data['id']
        self.message=data['message']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.user_id=data['user_id']
        self.friend_id=data['friend_id']
        
        
    @classmethod
    def create(cls,data) :
        query="INSERT INTO messages (message,user_id,friend_id) VALUES %(message)s,%(user_id)s,%(friend_id)s ;"
        return connectToMySQL(DB).query_db(query,data)
    
    
    @classmethod
    def get_all(cls) :
        query="SELECT * FROM messages ;"
        results=connectToMySQL(DB).query_db(query)
        all_messages=[]
        for row in results :
            message=cls(row)
            all_messages.append(message)
        return all_messages 