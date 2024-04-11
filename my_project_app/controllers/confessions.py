from flask import render_template,request, redirect,session,flash
from my_project_app import app
from my_project_app.models.confession import Confession
from my_project_app.models.user import User



@app.route('/confession/new')
def new_confession():
    data = {
        'id': session['user_id']
    }
    user = User.show_user(data)
    return render_template('new_confession.html',user=user)

@app.route('/create/new', methods= ['POST'])
def create_shows():
    title =  request.form['title']
    
    data = {
        "title" :title,
        "category" : request.form["category"],
        "story": request.form["story"],
        "user_id": request.form["user_id"]
    }
    Confession.save_confession(data)
    return redirect('/dashboard')

@app.route('/confession/<int:id>')
def show_confession(id):
    data = {
        'id': id
    }
    confession = Confession.show_one_confession(data)
    return render_template('one_confession.html',confession=confession)
