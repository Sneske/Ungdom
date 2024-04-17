from flask import Flask, render_template, redirect, url_for, flash, session, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
from flask_wtf import FlaskForm
import base64
import os

database = os.getcwd() + '/events.db'
app = Flask(__name__)
app.config['SECRET_KEY'] = '5c59e31d0c4e528fe5647908e15807a5' # ændrer scret key instillingen for at beskytte hjemmeside mod angreb
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# class der forbinder databasen, så det er mulig at hente og sende data til databasen.
class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'start': self.start.isoformat(),
            'end': self.end.isoformat()
        }


class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(6969), unique=True, nullable=False)
    password = db.Column(db.String(6969), nullable=False)



#FlaskForms og validaters    
class signupclass(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'LarsLarsen423'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder': '********'})
    confirmpassword = PasswordField('Bekæft Password', validators=[DataRequired(), EqualTo('password')], render_kw={'placeholder': '********'})
    submit = SubmitField('Sign Up')

class loginclass(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={'placeholder': 'LarsLarsen423'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder': '********'})
    submit = SubmitField('Login')


#Login og signup funktioner

# denne funktioner opretter en bruger
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    with app.app_context(): 
        form = signupclass()
        if form.validate_on_submit():
            if users.query.filter_by(username=form.username.data).first():
                flash('Brugernavn findes allerede. Brug et andet navn', 'error')
                return redirect(url_for('signup')) 
            hashed_password = generate_password_hash(form.password.data) # passwordet bliver hashed. det gør den fordi, hvis der skulle ske et uheld og databaserne bliver leaked på nettet, så skal man først dekryptere det før man kender passwordet
            new_user = users(username=form.username.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        return render_template('signup.html', form=form)

# denne funktioner logger in på en oprettede bruger 
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
    
@app.route('/profile')
def profile():
    if not session.get("username"):
        return render_template("login.html")
    else:
        return render_template('profile.html')

#logout funktion sletter en session. session bruger vi til at holde styr på hvem er logget ind.
@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")


@app.route('/')
def index():
    events = Event.query.all()
    return render_template('calendar.html', events=[event.to_dict() for event in events])

@app.route('/add_event', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        title = request.form['title']
        start = datetime.fromisoformat(request.form['start'])
        end = datetime.fromisoformat(request.form['end'])
        event = Event(title=title, start=start, end=end)
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_event.html')

@app.route('/update_event', methods=['POST'])
def update_event():
    data = request.get_json()
    event = Event.query.get(int(data['id']))
    if event:
        event.start = datetime.fromisoformat(data['start'])
        event.end = datetime.fromisoformat(data['end'] if data['end'] else data['start'])
        db.session.commit()
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)