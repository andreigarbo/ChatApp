from flask import Flask, jsonify, request, send_file, render_template, redirect, flash, current_app, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import models
from flask_session import Session
from persistence import database_access
import lib
import matplotlib.pyplot as plt
import PIL
import hashlib
import os
import atexit
import json
from flask_cors import CORS
import jwt

template_dir = os.path.abspath('../templates/')
app = Flask(__name__,template_folder=template_dir,static_folder='static')
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key ="abc123"
CORS(app, origins=['http://localhost:3000'])

active_users=[]

#app.use_static_folder('static')

db = database_access.Database_access()

login_manager = LoginManager()
login_manager.init_app(app)

def shutdown_handler():
    db.logout_all_users()

atexit.register(shutdown_handler)
class User():
    def __init__(self, username):
        self.username = username
        db.set_logged_on_status(username,"True")

    def is_active(self):
        return True
    
    def get_id(self):
        return self.username
    
    def is_authenticated(self):
        if db.get_logged_on_status(self.username) == "True":
            return True
        else:
            return False
        
    def is_anonymous(self):
        return False
        

@login_manager.user_loader
def load_user(user_id):
    user = lib.get_user_object(user_id,db)
    if user != None:
        user_obj = User(user['username'])
        return user_obj
    else:
        return None

#@app.before_request
#def before_request():
#    if not current_user.is_authenticated and request.endpoint !="login" and request.endpoint != "static":
#        return redirect('login')

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    user = lib.get_user_object(username,db)

    if user and user['password'] == hashlib.sha256(password.encode('utf-8')).hexdigest():
        user_obj = User(user['username'])
        login_user(user_obj)
        token = jwt.encode({'user_id': username}, app.secret_key, algorithm='HS256')
        print(token)
        return jsonify({'token': token, 'is_admin' : lib.is_admin(username,db)})
    else:
        return jsonify({'status' :'error', 'reason': 'Invalid credentials'}), 401


@app.route('/logout', methods=['POST'])
#@login_required
def logout():
    token = request.headers.get('Authorization')
    print(token)
    #db.set_logged_on_status(current_user.username, 'False')
    logout_user()
    return jsonify({'status' : 'Logged out'})

@app.route('/', methods=['GET'])
@login_required
def index():
    users = lib.get_list_of_users(db)
    active_user = current_user.username
    messages = []
    return render_template('main_view.html', users=users, active_user=active_user, messages=messages)

@app.route('/get-user-list', methods=['GET'])
def get_users():
    user_list=lib.get_list_of_users(db)
    response = {'users': user_list}
    return jsonify(response)


@app.route('/generate-message-graph', methods=['GET'])
def generate_graph():
    graph_dict = lib.generate_message_graph(db)
    username_list=list(graph_dict.keys())
    value_list = list(graph_dict.values())
    fig, ax = plt.subplots()
    ax.bar(username_list, value_list)
    ax.set_xlabel('User')
    ax.set_ylabel('Number of messages sent')
    ax.set_title('Message graph')
    fig.savefig('message_graph.png')
    return send_file('message_graph.png',mimetype='image/png')

@app.route('/messages-for-user/<username>', methods=['GET'])
def get_messages_for_user(username):
    messages_for_user = lib.get_all_user_messages(username,db)
    response = {'user' : username, 
                'messages' : messages_for_user}
    return jsonify(response)

@app.route('/load_messages/<username>')
def load_messages(username):
    # Load messages for specified user from database
    messages = lib.get_message(username,current_user.username,db)   
    messages_json = json.dumps(messages)
    return messages_json

@app.route('/create-user', methods=['POST'])
def create_user():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')
    if not lib.user_exist(username,db) and lib.email_validator(email):
        if lib.create_user(username, hashlib.sha256(password.encode('utf-8')).hexdigest(),email,db) == True:
            lib.send_signup_mail(email)
            status = 'SUCCESS'
            message = 'User created'
            return jsonify({'status' : 'success'})
        else:
            status = 'FAIL'
            message = 'An error occured'
            return jsonify({'status' : 'fail', 'reason' : 'An error occured'}), 401
    elif lib.user_exist(username,db):
        status = 'FAIL'
        message = 'User already exists'
        return jsonify({'status' : 'fail', 'reason' : 'User already exists'}), 401

    elif not lib.email_validator(email):
        status = 'FAIL'
        message = 'Invalid email address'
        return jsonify({'status' : 'fail', 'reason' : 'Invalid email address'}), 401



@app.route('/update-password/<username>/<oldpassword>/<newpassword>', methods=['POST'])
def update_password(username,oldpassword,newpassword):
    status = lib.update_password(username,oldpassword,newpassword,db)
    response={
        'username' : username,
        'status' : status
    }
    return jsonify(response)

@app.route('/messages-between/<userone>/<usertwo>', methods=['GET'])
def get_messages_between(userone,usertwo):
    messages = lib.get_message(userone,usertwo,db)
    response={
        'userone':userone,
        'usertwo':usertwo,
        'messages':messages
    } 
    return jsonify(response)

@app.route('/send-message/<fromuser_send>/<touser_send>/<text_send>', methods=['POST'])
def send_message(fromuser_send, touser_send, text_send):
    lib.http_send_message(touser_send,fromuser_send,text_send,db)
    response={
        'from-user':fromuser_send,
        'to-user':touser_send,
        'message': text_send
    }
    return jsonify(response)

@app.route('/delete-user', methods=['POST'])
def delete_user():
    username = request.json.get('user')
    sof = lib.delete_user(username,db)
    if sof == False:
        status = 'SUCCESS'
    else:
        status = 'FAIL'
    response={
        'username':username,
        'status':status
    }
    return jsonify(response)

@app.route('/admin-change-password', methods=['POST'])
def admin_change_password():
    username = request.json.get('selectedUser')
    npass = request.json.get('password')
    if lib.admin_change_password(username,hashlib.sha256(npass.encode('utf-8')).hexdigest(),db) == True:
        return jsonify({'status' : "Success"})
    else:
        return jsonify({'status' : 'Failed'})


if __name__ == '__main__':
    app.run(debug=True, port=8000)