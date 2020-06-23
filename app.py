from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_heroku import Heroku

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://mhofpthgpwaepc:79bfef69684a1b783ad07e4fe3235a2620436e6595dbab96f2a16e12b72bac7c@ec2-34-230-231-71.compute-1.amazonaws.com:5432/de5auk0hvftiku'
db = SQLAlchemy(app)
ma = Marshmallow(app)

heroku = Heroku(app)
CORS(app)

class Month(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer, unique=True, nullable=False)
    month = db.Column(db.String(), unique=False, nullable=False)
    daysInMonth = db.Column(db.Integer, unique=False, nullable=False)
    daysInPreviousMonth = db.Column(db.Integer, unique=False, nullable=False)
    startDay = db.Column(db.Integer, unique=False, nullable=False)
    year = db.Column(db.Integer, unique=False, nullable=False)

    def __init__(self, position, month, daysInMonth, daysInPreviousMonth, startDay, year):
        self.position = position
        self.month = month
        self.daysInMonth = daysInMonth
        self.daysInPreviousMonth = daysInPreviousMonth
        self.startDay = startDay
        self.year = year

class MonthSchema(ma.Schema):
    class Meta:
        fields = ('id', 'position', 'month', 'daysInMonth', 'daysInPreviousMonth', 'startDay', 'year')


month_schema = MonthSchema()
months_schema = MonthSchema(many=True)

class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text=db.Column(db.String(), unique=False, nullable=False)
    date = db.Column(db.Integer, nullable=False)
    month = db.Column(db.String(), nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def __init__(self, text, date, month, year):
        self.text = text
        self.date = date
        self.month = month
        self.year = year

class ReminderSchema(ma.Schema):
    class Meta:
        fields = ("id", "text", "date", "month", "year")

reminder_schema = ReminderSchema()
reminders_schema = ReminderSchema(many=True)

@app.route("/reminder/add", methods=['POST'])
def add_reminder():
    if request.content_type != "application/json":
        return jsonify("Error: Data must be sent as JSON")

    post_data = request.get_json()
    text = post_data.get("text")
    date = post_data.get("date")
    month = post_data.get("month")
    year = post_data.get("year")

    record = Reminder(text, date, month, year)
    db.session.add(record)
    db.session.commit()

    return jsonify("Reminder added successfully")

@app.route("/reminder/get", methods=['GET'])
def get_reminders():
    all_reminders = db.session.query(Reminder).all()
    return jsonify(reminders_schema.dump(all_reminders))

@app.route('/reminder/get/<id>', methods=['GET'])
def get_reminder(id):
    reminder = Reminder.query.get(id)
    return reminder_schema.jsonify(reminder)

@app.route("/month/add", methods=['POST'])
def add_month():
    if request.content_type == "application/json":
        post_data = request.get_json()
        position = post_data.get("position")
        month = post_data.get('month')
        daysInMonth = post_data.get('daysInMonth')
        daysInPreviousMonth = post_data.get('daysInPreviousMonth')
        startDay = post_data.get("startDay")
        year = post_data.get('year')

        record = Month(position, month, daysInMonth, daysInPreviousMonth, startDay, year)
        db.session.add(record)
        db.session.commit()

        return jsonify("Month added successfully")
    else:
        return jsonify("Error: Data must be sent as JSON")

@app.route("/month/get", methods=["GET"])
def get_all_months():
    all_months = db.session.query(Month).all()
    return jsonify(months_schema.dump(all_months))




if __name__ == "__main__":
    app.run(debug=True)