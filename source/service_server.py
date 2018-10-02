from flask import Flask, jsonify, abort, request
import jwt
import requests
from functools import wraps

app = Flask(__name__)
secret_key = 'secret_key'

def jwt_token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # header 차있는지
        # token이 정상적인건지
        if not 'Authorization' in request.headers:
            return jsonify({
                'msg': 'token is not given'
            }), 400
        token = request.headers['Authorization']
        try:
            decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])
        except:
            return jsonify({
                'msg': 'Invalid token given'
            }), 400
        kwargs['decoded_token'] = decoded_token
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return "Hello Pycon Server"

@app.route('/login')
def login():
    r = requests.get("http://127.0.0.1:5001/get_token")
    rsp_json = r.json()
    token = rsp_json['access_token']

    return jsonify({
        'access_token': token,
        'msg': "Successfully login"
    }), 200

@app.route("/protected_service")
@jwt_token_required
def protected_service(**kwargs):
    return jsonify({
        'msg': 'hello protected user'
    }), 200

@app.route("/v3")
@jwt_token_required
def other_scope_service(**kwargs):
    token = kwargs['decoded_token']
    if 'v3' in token['scope']:
        # service logic
        return jsonify({
            'msg': 'welcome v3 user'
        }), 200
    else:
        return jsonify({
            'msg': 'You are not authorized'
        }), 401

app.run()