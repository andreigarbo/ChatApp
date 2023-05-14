import re
import sys
import json
import datetime
import os
sys.path.append('../persistence')
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import hashlib

def send_email(from_addr, to_addr, subject, body, attachment_path=None):
    # Set up the email message
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject

    body_text = MIMEText(body)
    msg.attach(body_text)

    if attachment_path:
        with open(attachment_path, 'rb') as f:
            file_data = f.read()
            attachment = MIMEApplication(file_data, Name='report.pdf')
            attachment['Content-Disposition'] = f'attachment; filename="report.pdf"'
            msg.attach(attachment)

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login('alerta.senzor@gmail.com', 'ABCDEFG_1')
        smtp.send_message(msg)

def email_validator(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if(re.fullmatch(regex, email)):
        return True
    return False

def user_exist(user,db):
    return db.check_if_user_exists(user)

def create_user(username,hashpass,email,db):
    db.add_user(username,hashpass,email)
    return True

def transmit_message(conn, message):
    conn.send(message.encode())
    #ack = conn.recv(1024)

def validate_password(username,hash,db):
    if db.get_password_by_user(username) == hash:
        return True
    return False

def send_signup_mail(email):
    try:
        send_email("alerta.senzor@gmail.com", email, "Created ChatApp Account", "Thank you for creating an account!", None)
        print("SENT MAIL")
    except:
        print("MAIL ERROR")
        pass

def send_message(touser, fromuser, message, user_dict,db):
    db.add_message(fromuser,touser,message)
    for conn, username in user_dict.items():
        if username==touser:
            reqdict = {
                'type' : 'ask-for-messages'
            }
            reqjson = json.dumps(reqdict)
            transmit_message(conn,reqjson)

def http_send_message(touser,fromuser,message,db):
    db.add_message(fromuser,touser,message)

def get_list_of_users(db):
    return db.get_user_list()

def get_message(fromuser,touser,db):
    return db.get_user_messages(fromuser,touser)

def delete_user(delete,db):
    return db.remove_user_from_database(delete)

def get_user_admin(user,db):
    return db.get_user_or_admin(user)

def get_message_report(user,db):
    messages = db.get_messages_report(user)
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{timestamp}.txt"
    folder_path = './reports'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    filename = f'{timestamp}.txt'
    file_path = os.path.join(folder_path, filename)
    print(messages)
    print(file_path)
    write_to_file(messages, file_path)

def get_all_user_messages(user,db):
    messages = db.get_messages_report(user)
    return messages

def write_to_file(data_dict, filename):
        with open(filename, 'w') as f:
            for i in range(len(data_dict['sender'])):
                sender_name = data_dict['sender'][i]
                receiver_name = data_dict['receiver'][i]
                message_content = data_dict['text_content'][i]
                f.write(f"message sent from {sender_name} to {receiver_name}: {message_content}\n")
                
def generate_message_graph(db):
    user_list = get_list_of_users(db)
    graph_dict={}
    for user in user_list:
        number = db.count_sender_messages(user)
        graph_dict[user] = number
    return graph_dict

def update_password(username, old, new, db):
    hold = hashlib.sha256(old.encode('utf-8')).hexdigest()
    hnew = hashlib.sha256(new.encode('utf-8')).hexdigest()
    return db.update_password(username,hold,hnew)
    
def get_user_object(username,db):
    if user_exist(username,db):
        user = {}
        password = db.get_password_by_user(username)
        email = db.get_email_by_username(username)
        id=db.get_id_by_username(username)
        user["username"]=username
        user["password"]=password
        user["email"]=email
        user["id"]=id
        print(user)
        return user
    else:
        return None
    
def is_admin(username, db):
    return db.is_admin(username)

def admin_change_password(username,password,db):
    return db.admin_change_password(username,password)