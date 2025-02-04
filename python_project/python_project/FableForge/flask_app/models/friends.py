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
    def get_friends_by_user(cls, user_id):
        query = """
        SELECT users.id, users.username, users.image, users.interests 
        FROM friends
        JOIN users ON (friends.friend_id = users.id OR friends.user_id = users.id)
        WHERE (%(user_id)s IN (friends.user_id, friends.friend_id)) 
        AND users.id != %(user_id)s;
        """
        data = {'user_id': user_id}
        results = connectToMySQL(DB).query_db(query, data)
        return results

    @classmethod
    def get_one_friend(cls,friend_id):
        query = "SELECT * FROM users WHERE id = %(friend_id)s"
        data = {'friend_id': friend_id}
        result = connectToMySQL(DB).query_db(query, data)
        if result:
            return result[0]
        return None

    
    @classmethod
    def remove_friend(cls, user_id, friend_id):
        query = """
            DELETE FROM friends
            WHERE (user_id = %(user_id)s AND friend_id = %(friend_id)s)
            OR (user_id = %(friend_id)s AND friend_id = %(user_id)s);
        """
        data = {
            'user_id': user_id,
            'friend_id': friend_id
        }
        connectToMySQL(DB).query_db(query, data)