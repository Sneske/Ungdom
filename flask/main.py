
from flask import Flask, render_template, redirect, url_for, flash, session, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
import os
import time
from apscheduler.schedulers.background import BackgroundScheduler
from flask_login import login_required, current_user, login_manager
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import base64
from datetime import datetime, timedelta, timezone
from flask_socketio import SocketIO, emit
import RPi.GPIO as GPIO


database = os.getcwd() + '/database.db' 
app = Flask(__name__) 
app.config['SECRET_KEY'] = '45gt4un3tn3g945hg0945graseiurn09wgr4wu90h45hg0' 
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database}' 
db = SQLAlchemy(app) 

socketio = SocketIO(app)

scheduler = BackgroundScheduler()
scheduler.start()

# Database Data Fetch
class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(6969), unique=True, nullable=False)
    password = db.Column(db.String(6969), nullable=False)

class kalender(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    beskrivelse = db.Column(db.String(6969))
    pris = db.Column(db.Integer())
    udlobsdato = db.Column(db.Integer())
    img = db.Column(db.Text, unique=True, nullable=False)
    imgname = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    kategori = db.Column(db.String(6969))
    name = db.Column(db.String(6969))
    tid = db.Column(db.DateTime, nullable=True)

# Form Site Validaters
class signupclass(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'LarsLarsen423'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder': '********'})
    confirmpassword = PasswordField('Bekæft Password', validators=[DataRequired(), EqualTo('password')], render_kw={'placeholder': '********'})
    submit = SubmitField('Sign Up')

class loginclass(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={'placeholder': 'LarsLarsen423'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder': '********'})
    submit = SubmitField('Login')



#Funktioner


def custom_b64encode(data):
    if data is not None:
        return base64.b64encode(data).decode('utf-8')
    return ''

app.jinja_env.filters['custom_b64encode'] = custom_b64encode


#app routes

#homepage
@app.route("/", methods=['GET'])
def produkter():
    products = varer.query.all()

    statusColor = []
    for product in products:
        if(isinstance(product.tid, str)):
           product.tid = (datetime.strptime(product.tid, '%Y-%m-%d %H:%M:%S.%f'))

        if datetime.utcnow() > product.tid: 
            statusColor.append('border-red-500')
        else:
            statusColor.append('border-green-500')

    return render_template("produkter.html", products=products, statusColor=statusColor, zip=zip, datetime=datetime)

#signup and login
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    with app.app_context(): 
        form = signupclass()
        if form.validate_on_submit():
            findesuser = users.query.filter_by(username=form.username.data).first()
            if findesuser:
                flash('Brugernavn findes allerede. Brug et andet navn', 'error')
                return redirect(url_for('signup')) 
            hashed_password = generate_password_hash(form.password.data) # passwordet bliver hashed. det gør den fordi, hvis der skulle ske et uheld og databaserne bliver leaked på nettet, så skal man først dekryptere det før man kender passwordet
            new_user = users(username=form.username.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    with app.app_context():
        form = loginclass()
        if form.validate_on_submit():
            user = users.query.filter_by(username=form.username.data).first()
            if users.query.filter_by(username=form.username.data).first() and check_password_hash(user.password, form.password.data):
                session["username"] = form.username.data
                return redirect(url_for('profile'))
            else:
                flash('Brugernavn eller Password er forkert', 'error')
                return redirect(url_for('login'))
        return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/tilfoj", methods=['GET', 'POST'])
def tilfoj():
    with app.app_context():
        form = varerclass()
        if form.validate_on_submit():
            # billede funktion
            pic = request.files["pic"]

            filename = secure_filename(pic.filename)
            mimetype = pic.mimetype

            # nedtællings funktion
            countdown_hours = int(form.nedtimer.data) if form.nedtimer.data else 0
            countdown_minutes = int(form.nedminutter.data) if form.nedminutter.data else 0

            countdown_seconds = (countdown_hours) * 3600 + countdown_minutes * 60
            
            end_time = datetime.utcnow() + timedelta(seconds=countdown_seconds)
            kar = varer(beskrivelse=form.beskrivelse.data, pris=form.pris.data, img=pic.read(), mimetype=mimetype, imgname=filename, tid=end_time, kategori=form.kategorier.data)
            db.session.add(kar)
            
            db.session.commit()

            db.session.refresh(kar)

            productID = kar.id

            scheduler.add_job(moveFinishedAuction, "date", args=[productID], next_run_time=end_time + timedelta(seconds=3600))

        return render_template('tilfoj.html', form=form)
