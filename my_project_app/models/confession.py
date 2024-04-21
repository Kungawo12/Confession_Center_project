from my_project_app.config.mysqlconnection import connectToMySQL
from my_project_app.models.user import User
from flask import flash


class Confession:
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.category = data['category']
        self.story = data['story']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None
        self.comments= None
    
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
    
    @classmethod
    def get_confessions_by_category(cls, category):
        query = """
            SELECT * FROM confessions
            JOIN users ON confessions.user_id = users.id
            WHERE confessions.category = %(category)s;
        """
        data = {'category': category}
        results = connectToMySQL('myProject_db').query_db(query, data)
        
        confessions = []
        for row in results:
            confession_data = {
                "id": row["id"],
                "title": row["title"],
                "category": row["category"],
                "story": row["story"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
                # You can include user data if needed
                "user": {
                    "id": row["user_id"],
                    "first_name": row["first_name"],
                    "last_name": row["last_name"],
                    "email": row["email"],
                    "password": row["password"],
                    # Add other user fields as needed
                }
            }
            confessions.append(confession_data)
        
        return confessions
        
    @classmethod
    def update_confession(cls,data):
        query= """UPDATE confessions SET title = %(title)s, category = %(category)s, story = %(story)s
                WHERE id = %(id)s;
            """
        return connectToMySQL('myProject_db').query_db(query,data)
    
    @classmethod
    def delete_confession(cls,data):
        query= "DELETE FROM confessions WHERE id = %(id)s;"
        return connectToMySQL('myProject_db').query_db(query,data)
    
    @classmethod
    def save_comment(cls,data):
        query= """INSERT INTO comments(text,confession_id,user_id)
                VALUES
                (%(text)s,%(confession_id)s,%(user_id)s)
                """
        return connectToMySQL('myProject_db').query_db(query,data)
    
    @classmethod
    def get_all_comments(cls,data):
        query= """SELECT * FROM comments
                LEFT JOIN users on comments.user_id = users.id
                LEFT JOIN confessions on comments.confession_id = confessions.id
                WHERE comments.confession_id = %(confession_id)s;
            """
        results = connectToMySQL('myProject_db').query_db(query,data)
        comments =[]
        for row in results:
            comment_data = {
                "comment_id": row["id"],
                "comment_text": row["text"],
                "confession_id": row["confessions.id"],
                "user_id": row["users.id"],
                "created_at": row["created_at"],
                "updated_at": row['updated_at'],
                }
            comments.append(comment_data)
        return comments
    
    @classmethod
    def like_confession(cls, data):
        # Check if a like from this user already exists
        query = """SELECT * FROM likes WHERE user_id = %(user_id)s AND confession_id = %(confession_id)s"""
        existing_like = connectToMySQL('myProject_db').query_db(query, data)

        if not existing_like:  # If no existing like was found
            # Insert a new like
            query = """INSERT INTO likes(user_id, confession_id) VALUES (%(user_id)s, %(confession_id)s)"""
            connectToMySQL('myProject_db').query_db(query, data)
    
    @classmethod
    def get_like_count(cls, confession_id):
        query = "SELECT COUNT(*) as count FROM likes WHERE confession_id = %(confession_id)s"
        data = {'confession_id': confession_id}
        result = connectToMySQL('myProject_db').query_db(query, data)
        return result[0]['count']
    
    @staticmethod
    def get_all_categories():
        query = "SELECT DISTINCT category FROM confessions;"
        results = connectToMySQL('myProject_db').query_db(query)
        categories = [row['category'] for row in results]
        return categories
    
    @staticmethod
    def validate_confession(data):
        is_valid = True
        if len(data['title']) < 3:
            flash("Title must be at least 3 characters.", "confession")
            is_valid = False
        if len(data['category']) < 3:
            flash("Category must be at least 3 characters.", "confession")
            is_valid = False
        if len(data['story']) < 20:
            flash("Story must be at least 20 characters.", "confession")
            is_valid = False
        return is_valid