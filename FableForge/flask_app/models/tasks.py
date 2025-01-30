from flask_app.config.mySQLConnection import connectToMySQL
from flask_app import DB
from flask import flash

class Task:
    def __init__(self, data):
        self.id = data['id']
        self.task_name = data['task_name']
        self.task_description = data['task_description']
        self.task_difficulty = data['task_difficulty']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def create(cls, data):
        query = """INSERT INTO tasks (task_name, task_description, task_difficulty, user_id) 
                   VALUES (%(task_name)s, %(task_description)s, %(task_difficulty)s, %(user_id)s);"""
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM tasks;"
        results = connectToMySQL(DB).query_db(query)
        all_tasks = []
        for row in results:
            task = cls(row)
            all_tasks.append(task)
        return all_tasks

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM tasks WHERE id=%(id)s;"
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def get_user_tasks(cls, data):
        query = "SELECT * FROM tasks WHERE user_id=%(user_id)s;"
        result = connectToMySQL(DB).query_db(query, data)
        all_tasks = []
        for row in result:
            task = cls(row)
            all_tasks.append(task)
        return all_tasks

    @classmethod
    def lvl_up(cls, data):
        query = "UPDATE users SET exp = exp + 100 WHERE id=%(id)s;"
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def lvl_plus(cls, data):
        query = "UPDATE users SET char_lvl = char_lvl + 1 WHERE id=%(id)s;"
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def reset_exp(cls, data):
        query = "UPDATE users SET exp = 0 WHERE id=%(id)s;"
        return connectToMySQL(DB).query_db(query, data)
    
    @staticmethod
    def validate_task(data):
        is_valid = True
        if data['task_name'] == "":
            is_valid = False
            flash("Quest name should not be left BLANK", "task_name_validation")
        return is_valid

