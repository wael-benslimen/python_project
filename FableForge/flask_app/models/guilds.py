from flask_app.config.mySQLConnection import connectToMySQL
from flask_app import DB



class Guild :
    def __init__(self,data) :
        self.id=data['id']
        self.guild_name=data['guild_name']
        self.guild_bio=data['guild_bio']
        self.location=data['location']
        self.created_at=data['created_at']
        self.updated_at=data['updated_it']
        
        
    @classmethod
    def create(cls,data) :
        query="""INSERT INTO guilds (guild_name,guild_bio,location)
        VALUES (%(guild_name)s,%(guild_bio)s,%(location)s);"""
        return connectToMySQL(DB).query_db(query,data)
    
    
    @classmethod
    def get_all(cls) :
        query="SELECT * FROM guilds ;"
        results = connectToMySQL(DB).query_db(query)
        all_guilds=[]
        for row in results :
            guild=cls(row)
            all_guilds.append(guild)
        return all_guilds
    
    
    @classmethod
    def delete(cls,data) :
        query="DELETE FOM guilds WHERE id=%(id)s ;"
        connectToMySQL(DB).query_db(query,data)