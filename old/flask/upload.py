# https://python.plainenglish.io/python-flask-allowing-users-to-upload-images-44e7f3656200
# https://www.geeksforgeeks.org/python-pillow-tutorial/
from flask import Flask, render_template, redirect, url_for, flash, session, request
from flask_sqlalchemy import SQLAlchemy
import os

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash

database = os.getcwd() + '/database.db'
app = Flask(__name__)
app.config['SECRET_KEY'] = '5c59e31d0c4e528fe5647908e15807a5'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database}' 
db = SQLAlchemy(app)
 
@app.route('/', methods=("POST", "GET"))
def uploadFile():
    ALLOWED_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG']
    if request.method == 'GET':
        return render_template('upload.html', msg='')
    image = request.files['file']
    file_name, file_extension = os.path.splitext(image.filename)
    if file_extension in ALLOWED_EXTENSIONS:
        img = Image.open(image)
        img.thumbnail((400, 400))
        img = img.rotate(180)
        img.save("uploads/"+image.filename, "PNG")
    else:
        flash("Ikke tilladt filtype!")
        return render_template('login.html', msg='Billedet er ikke uploaded!')
    return render_template('login.html', msg='Billedet er uploaded')

if __name__ == '__main__': 
    app.run(debug=True) 