from my_project_app import app
from my_project_app.controllers import users, confessions

if __name__ == "__main__":
    app.run(debug= True, port=5001)