from flask import Flask, jsonify
import jwt
import datetime

app = Flask(__name__)
secret_key = 'secret_key'

@app.route('/')
def index():
    return "Hello auth server"

@app.route("/get_token")
def get_token():
    # db 작업
    issuer = 'pycon_tutorial'
    subject = 'localhost:5000/v1'
    date_time_obj = datetime.datetime
    exp_time = date_time_obj.timestamp(date_time_obj.utcnow() + datetime.timedelta(hours=24))
    scope = ['v1', 'v2']
    payload = {
        'sub': subject,
        'iss': issuer,
        'exp': int(exp_time),
        'scope': scope
    }
    token = jwt.encode(payload, secret_key, algorithm='HS256')

    return jsonify({
        'msg': 'token is generated',
        'access_token': str(token)
    }), 201

@app.route("/admin_login")
def admin_login():
    issuer = 'pycon_tutorial'
    subject = 'localhost:5000/v1'
    date_time_obj = datetime.datetime
    exp_time = date_time_obj.timestamp(date_time_obj.utcnow() + datetime.timedelta(hours=24))
    scope = ['v1', 'v2', 'v3']
    payload = {
        'sub': subject,
        'iss': issuer,
        'exp': int(exp_time),
        'scope': scope
    }
    token = jwt.encode(payload, secret_key, algorithm='HS256')

    return jsonify({
        'msg': 'token is generated',
        'access_token': str(token)
    }), 201

app.run(port=5001)