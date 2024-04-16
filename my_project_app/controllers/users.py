from flask import render_template,request, redirect,session,flash
from my_project_app.models.user import User
from my_project_app.models.confession import Confession

from my_project_app import app
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("home.html")

@app.route('/login')
def user_login():
    return render_template("login.html")

@app.route('/register')
def user_register():
    return render_template('registration.html')

@app.route('/dashboard')   
def confessions():
    if 'user_id' not in session:
        flash('Please log in to view this page', "login")
        return redirect('/login')
    data = {
        'id': session['user_id']
    }
    all_confession= Confession.get_all_confession()
    return render_template('dashboard.html', user= User.show_user(data),confessions = all_confession)
    

@app.route('/user/register', methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/register')
    user_data = {
        "email": request.form['email']
    }
    user = User.get_by_email(user_data)
    if user:
        flash("Email already in use, please log in", 'email')
        return redirect('/')
    data={
        'first_name': request.form['first_name'], 
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password']) 
    }
    id = User.save(data)
    session['user_id'] = id
    return redirect('/dashboard')

@app.route('/user/login', methods = ['POST'])
def login():
    if not User.validate_login(request.form):
        return redirect('/login')
    data = {
        "email": request.form['log_email']
    }
    user = User.get_by_email(data)
    
    if not user:
        flash('Invalid Email', "login")
        return redirect('/login')
    if not bcrypt.check_password_hash(user.password, request.form['log_password']):
        flash('Invalid Password', "login")
        return redirect('/')
    session['user_id'] = user.id
    
    return redirect('/dashboard')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


