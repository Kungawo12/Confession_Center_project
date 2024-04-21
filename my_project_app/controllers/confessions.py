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
    if not Confession.validate_confession(request.form):
        return redirect('/confession/new')
    title =  request.form['title']
    data = {
        "title" :title,
        "category" : request.form["category"],
        "story": request.form["story"],
        "user_id": request.form["user_id"]
    }
    Confession.save_confession(data)
    return redirect('/dashboard')

@app.route('/confession/<int:id>', methods=['GET','POST'])
def show_confession(id):
    if request.method == 'POST':
        user_id = request.form.get('user_id')  # Get user_id from form data
        Confession.like_confession({'user_id': user_id, 'confession_id': id})
        return redirect('/confession/'+str(id))  # Redirect back to the same page

    data = {
        'id': id
    }
    user_comment = Confession.get_all_comments({"confession_id": id})
    confession = Confession.show_one_confession(data)
    like_count = Confession.get_like_count(id)
    return render_template('one_confession.html',confession=confession,comments=user_comment,like_count=like_count)

@app.route('/confession/edit/<int:id>')
def edit_confession(id):
    user_data = {
        'id': session['user_id']
    }
    data={
        "id":id
    }
    return render_template('edit_confession.html',confession=Confession.show_one_confession(data),user=User.show_user(user_data))

@app.route('/confession/update/<int:id>', methods=['POST'])
def update_confession(id):
    if not Confession.validate_confession(request.form):
        return redirect('/confession/edit/'+str(id))
    data = {
        "id": id,
        "title": request.form['title'],
        "category": request.form['category'],
        "story": request.form['story']
    }
    Confession.update_confession(data)
    return redirect('/dashboard')

@app.route('/confession/delete/<int:id>')
def delete_confession(id):
    data = {
        'id': id
    }
    Confession.delete_confession(data)
    return redirect('/dashboard')

@app.route('/comment/<int:id>', methods=['POST'])
def get_comments(id):
    data = {
        'user_id': session['user_id'],
        'confession_id': id,
        'text': request.form['text']
    }
    Confession.save_comment(data)
    return redirect('/confession/'+str(id))
    
@app.route('/like_confession', methods=['POST'])
def like_confession():
    user_id = request.form.get('user_id')
    confession_id = request.form.get('confession_id')
    data = {'user_id': user_id, 'confession_id': confession_id}
    Confession.like_confession(data)
    return redirect('/confession/'+str(confession_id))