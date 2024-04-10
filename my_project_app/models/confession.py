from my_project_app.config.mysqlconnection import connectToMySQL
from my_project_app.models.user import User
from flask import flash


class Confession:
    def __init(self,data):
        self.id = data['id']
        self.title = data['title']
        self.category = data['category']
        self.story = data['story']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None
    
    @classmethod
    def save_confession(cls,data):
        query= """INSERT INTO confessions(title,category,story,user_id)
                VALUES
                (%(title)s,%(category)s,%(story)s,%(user_id)s)
                """
        return connectToMySQL('myProject_db').query_db(query,data)
    
    @classmethod
    def get_all_confession(cls):
        query= """SELECT * FROM confessions
                LEFT JOIN users on confessions.user_id = users.id;
            """
        results = connectToMySQL('myProject_db').query_db(query)
        
        user_with_confession =[]
        for row in results:
            confession_data = Confession(row)
            user_data = User({
                "id": row["user_id"],
                "first_name": row["first_name"],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                "created_at": row["created_at"],
                "updated_at": row['updated_at']
            })
            confession_data.user = user_data
            
            user_with_confession.append(confession_data)
        return user_with_confession
    
    @classmethod
    def show_one_confession(cls,data):
        query= """SELECT * FROM confessions
                JOIN users on confessions.user_id = users.id
                WHERE confessions.id = %(id)s;
            """
        results = connectToMySQL('myProject_db').query_db(query,data)
        confession_dict =results[0]
        confession_obj = cls(confession_dict)
        user_obj = User({
                "id": confession_dict["user_id"],
                "first_name": confession_dict["first_name"],
                'last_name': confession_dict['last_name'],
                'email': confession_dict['email'],
                'password': confession_dict['password'],
                "created_at": confession_dict["created_at"],
                "updated_at": confession_dict['updated_at']
        })
        
        confession_obj.user = user_obj
        return confession_obj
        