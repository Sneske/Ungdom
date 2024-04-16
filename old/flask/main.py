#alle variabler
from flask import Flask, render_template, redirect, url_for, flash, session, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import login_required, current_user, login_manager
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import base64

database = os.getcwd() + '/database.db' #variable til at finde nuværende sti
print(database)
app = Flask(__name__) # flask variable til at lave indstillinger
app.config['SECRET_KEY'] = '5c59e31d0c4e528fe5647908e15807a5' # ændrer scret key instillingen for at beskytte hjemmeside mod angreb
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database}' # ændrer database instillingen ved at bruge "database" variable til at connect to databasen
db = SQLAlchemy(app) 


#database fetch
# connecter til databasens tables



class varer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    beskrivelse = db.Column(db.String(6969))
    pris = db.Column(db.Integer())
    udlobsdato = db.Column(db.Integer())
    img = db.Column(db.Text, unique=True, nullable=False)
    imgname = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)

class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(6969), unique=True, nullable=False)
    password = db.Column(db.String(6969), nullable=False)


#forms sider
# form sider er de inputs man gerne vil have brugeren skriver i
class varerclass(FlaskForm):
    beskrivelse = StringField('Skriv en beskrivelse af dit produkt', validators=[DataRequired()], render_kw={'placeholder': 'Eksempel: en smuk blå vase med grønne prikker'})
    pris = StringField('Skriv din pris', validators=[DataRequired()], render_kw={'placeholder': 'Eksempel: 20 kr'})
    udlobsdato = StringField('Tid for hvornår produktet udløber', validators=[DataRequired()], render_kw={'placeholder': 'Eksempel: 15/09/24'})
    submit = SubmitField('Sæt på auktion')

class signupclass(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'LarsLarsen423'})
    password = PasswordField('Password', validators=[DataRequired()])
    confirmpassword = PasswordField('Bekæft Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class loginclass(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')



def custom_b64encode(data):
    if data is not None:
        return base64.b64encode(data).decode('utf-8')
    return ''

app.jinja_env.filters['custom_b64encode'] = custom_b64encode

#app routes
#forside
@app.route("/")
def index():
    products = varer.query.all()
    return render_template("index.html", products=products)

productCategories = {
    "all" : "*"
}


#signup side
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    with app.app_context(): 
        form = signupclass()
        if form.validate_on_submit():
            hashed_password = generate_password_hash(form.password.data)
            new_user = users(username=form.username.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        return render_template('signup.html', form=form)

#login side
@app.route('/login', methods=['GET', 'POST'])
def login():
    with app.app_context():
        form = loginclass()
        if form.validate_on_submit():
            user = users.query.filter_by(username=form.username.data).first()
            if users.query.filter_by(username=form.username.data).first() and check_password_hash(user.password, form.password.data):
                session["username"] = form.username.data
                return redirect(url_for('profile'))
        return render_template('login.html', form=form)

#bruger kan se sin profil
@app.route('/profile')
def profile():
    if not session.get("username"):
        return render_template("login.html")
    else:
        return render_template('profile.html')


#logout funktion
@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

#her kan admin tilføje et produkt 
@app.route("/tilfoj", methods=['GET', 'POST'])
def tilfoj():
    with app.app_context():
        form = varerclass()
        if form.validate_on_submit():
            pic = request.files["pic"]

            #hvis ingen billede er uploaded så giver den en fejl 400
            #if not pic:
                #return "no pic uploaded", 400
    
            filename = secure_filename(pic.filename)
            mimetype = pic.mimetype
            kar = varer(beskrivelse=form.beskrivelse.data, pris=form.pris.data, udlobsdato=form.udlobsdato.data, img=pic.read(), mimetype=mimetype, imgname=filename)
            db.session.add(kar)
            db.session.commit()

        return render_template('tilfoj.html', form=form)



#start variable for at starte flask
if __name__ == '__main__': 
    app.run(debug=True)

#monaco font