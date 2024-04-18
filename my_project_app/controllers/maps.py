from flask import Flask, render_template
from my_project_app import app
import os
from dotenv import load_dotenv


load_dotenv()


@app.route('/maps')
def maps():
    # print(os.environ)
    api_key = os.environ.get('MAP_API_KEY')
    return render_template('maps.html', api_key = api_key)