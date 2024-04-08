from my_project_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.confessions = []
    
    @classmethod
    def get_all_users(cls):
        query= "SELECT * FROM users"
        results= connectToMySQL('belt_exam_db').query_db(query)
        users = []
        
        for user in results:
            users.append(cls(user))
        return users
    
    
    
    @classmethod
    def save(cls,data):
        query = """INSERT INTO users(first_name,last_name,email,password)
                    VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s);
        """
        return connectToMySQL('belt_exam_db').query_db(query,data)
    
    @classmethod
    def show_user(cls,data):
        query ="SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('belt_exam_db').query_db(query,data)
        return cls(results[0])
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('belt_exam_db').query_db(query,data)
        
        if len(results) < 1:
            return False
        return cls(results[0])
    
    # @ classmethod
    # def get_one_with_pies(cls,data):
    #     from belt_exam_flask_app.models.pie import Pie
    #     query = """
    #         SELECT * FROM users 
    #         LEFT JOIN pies on users.id = pies.user_id
    #         WHERE users.id = %(id)s
    #     """
    #     results = connectToMySQL('belt_exam_db').query_db(query,data)
        
    #     user = cls(results[0])
    #     for row in results:
    #         n = {
    #             "id" : row["pies.id"],
    #             "name" : row['name'],
    #             "filling" : row['filling'],
    #             "crust" : row['crust'],
    #             "created_at" : row['pies.created_at'],
    #             "updated_at" : row['pies.updated_at'],
    #         }
    #         user.pies.append(Pie(n))
    #     return user
    
    
    @staticmethod
    def validate_register(data):
        is_valid = True
        if len(data['first_name']) < 2 and len(data['last_name']) < 2 and not EMAIL_REGEX.match(data['email']) and len(data['password']) < 8 and not data['password'] == (data['confirm_password']):
            flash("All fields are required!",'register')
            is_valid=False
        else:
            if len(data['first_name']) < 2:
                flash('First name must at least 2 characters',"register")
                is_valid= False
            if len(data['last_name']) < 2:
                flash('Last name must be at least 2 characters', 'register')
                is_valid= False
            if not EMAIL_REGEX.match(data['email']):
                flash("Invalid email address",'register')
                is_valid= False
            if len(data['password']) < 8:
                flash('Password must be at least 8 characters', 'register')
                is_valid= False
            if not data['password'] == (data['confirm_password']):
                flash("password doesn't matched", 'register')
                is_valid= False
        return is_valid
    
    
    
    @staticmethod
    def validate_login(data):
        is_valid = True
        if not EMAIL_REGEX.match(data['log_email']):
            flash("Invalid email address!", "login")
            is_valid = False
        if len(data['log_password'])< 8:
            flash("Password must be at least 8 character", "login")
            is_valid = False
        return is_valid