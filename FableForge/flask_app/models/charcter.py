from flask_app.config.mySQLConnection import connectToMySQL



class Charcter:
    def __init__(self, data):
        self.id = data['id']
        self.type = data['class']
        self.lvl = data['lvl']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
        
        