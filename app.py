from multiprocessing import Event
import os, random, string
from datetime import datetime
from flask import Flask
from flask import jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "19090092.db"))

app = Flask(_name_)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

class Users(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(5), unique=True, nullable=False)
    password = db.Column(db.String(5), unique=True, nullable=False)
    token = db.Column(db.String(20), unique=True, nullable=False)


class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_creator = db.Column(db.String(50), unique=True, nullable=False)
    event_name = db.Column(db.String(50), unique=True, nullable=False)
    event_start_time = db.Column(db.Date, unique=True, nullable=False)
    event_end_time = db.Column(db.Date, unique=True, nullable=False)
    event_start_lat = db.Column(db.String(50),nullable=False)
    event_start_lng = db.Column(db.String(50),nullable=False)
    event_finish_lat = db.Column(db.String(50),nullable=False)
    event_finish_lng = db.Column(db.String(50),nullable=False)
    create_at = db.Column(db.Date, nullable=False,unique=True, default=datetime.now)

class Logs(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50),unique=True)
    event_name = db.Column(db.String(50))
    log_lat = db.Column(db.String(50))
    log_lng = db.Column(db.String(50))
    create_at = db.Column(db.DateTime(timezone=True), unique=True, default=func.now())


db.create_all()

#curl -i -X POST http://127.0.0.1:9200/api/v1/users/create -H 'Content-Type: application/json' -d '{"username":19090092, "password": 19090092}'

@app.route("/api/v1/users/create", methods=["POST"])
def create_user():
    username = request.json['username']
    password = request.json['password']

    newUsers = users(username=username, password=password)

    db.session.add(newUsers)
    db.session.commit() 
    return jsonify({
        'msg': 'berhasil tambah user',
        'username': username,
        'password' : password,
        'status': 200 
        })

#curl -i -X POST http://127.0.0.1:9200/api/v1/user/login -H 'Content-Type: application/json' -d '{"username":19090092, "password": 19090092}'

@app.route("/api/v1/user/login", methods=["POST"])
def login():
    username = request.json['username']
    password = request.json['password']

    user = Events.query.filter_by(username=username, password=password).first()

    if user:
        token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=100))
        
        Events.query.filter_by(username=username, password=password).update({'token': token})
        db.session.commit()

        return jsonify({
        'msg': 'Login berhasil',
        'username': username,
        'token': token,
        'status': 200 
        })

    else:
        return jsonify({
        'msg': 'Login gagal',
        'status': 401,
        })

#curl -i -X POST http://127.0.0.1:9200/api/v1/events/create -H 'Content-Type: application/json' -d '{"token": 7DFKN47ZPN, "event_name": tour danau toba, "event_start_time":2022-12-07 12:00:00, "event_end_time":2022-12-07 12:00:00, "event_start_lat": 40, "event_finish_lat": 42, "event_start_lng": 40, "event_finish_lng": 34}'
@app.route("/api/v1/events/create", methods=["POST"])
def create_event():

    token = request.json['token']

    token = Events.query.filter_by(token=token).first()
    if token:

        event_creator = request.json['event_creator']
        event_name = request.json['event_name']
        event_start_time = request.json['event_start_time']
        event_end_time = request.json['event_end_time']
        event_start_lat = request.json['event_start_lat']
        event_finish_lat = request.json['event_finish_lat']
        event_start_lng = request.json['event_start_lng']
        event_finish_lng = request.json['event_finish_lng']

        newEvents = Events(event_start_times=event_start_time, event_end_times=event_end_time, event_creators=event_creator, event_names=event_name, event_start_lat=event_start_lat, event_finish_lat=event_finish_lat, event_start_lng=event_start_lng, event_finish_lng=event_finish_lng)

        db.session.add()
        db.session.commit() 

        return newEvents, jsonify({
            'msg': 'berhasil tambah event'
            })

@app.route("/api/v1/events/log", methods=["POST"])
def event_log():
    token = request.json['token']

    token = Users.query.filter_by(token=token).first()

    if token:
        username = token.username
        event_name = request.json['event_name']
        log_lat = request.json['log_lat']
        log_lng = request.json['log_lng']

        db.session.add()
        db.session.commit() 

    return jsonify({
        'msg': 'Anda berhasil menambahkan posisi terbaru'
        })

@app.route("/api/v1/events/logs", methods=["GET"])
def event_logs():

    username = request.json['username']
    event_name = request.json['event_name']
   
    logs_event = Logs.query.filter_by(event_name=event_name).all()

    logs_status = {}

    for log in logs_event:
        dict_logs = []
        logs_status.append(dict_logs)
    
    return jsonify(logs_status)

if __name__ == '__main__':
    app.run(debug=False, port=9200)