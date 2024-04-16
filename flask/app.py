from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

database = os.getcwd() + '/events.db'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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