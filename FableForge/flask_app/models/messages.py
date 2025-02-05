from flask_app.config.mySQLConnection import connectToMySQL
from flask_app import DB 


class Message :
    def __init__(self,data) :
        self.id=data['id']
        self.message=data['message']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.user_id=data['user_id']
        
        
    @classmethod
    def create(cls,data) :
        query="INSERT INTO messages (message,user_id) VALUES (%(message)s,%(user_id)s) ;"
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
    
    
    @classmethod
    def get_latest(cls):
        query="SELECT * FROM messages ORDER BY created_at DESC LIMIT 10;"
        result=connectToMySQL(DB).query_db(query)
        latest_messages=[]
        for row in result :
            print(row)
            message=cls(row)
            latest_messages.append(message)
        print(latest_messages)
        return latest_messages