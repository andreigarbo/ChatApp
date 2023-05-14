#import business.models as ms
import hashlib
import persistence.database_access
import business.validators as vd
import sys
sys.path.append('../persistence')
import persistence.database_access
#from PIL import ImageTk, Image
import socket
from _thread import *
import base64
import json
import lib

list_of_clients = []
list_of_usernames = []
user_dict = {}

db_acc = persistence.database_access.Database_access()

def client_thread(conn, addr):
    while True:
        try:
            message = conn.recv(1024)
            if message:
                request_decoder(message, conn)
        except (ConnectionResetError, ConnectionAbortedError):
            print("Client ", addr, " disconnected")
            conn.close()
            list_of_clients.remove(conn)
            user_dict[conn]
            break
        except KeyboardInterrupt:
            print("Server shutdown initiated")
            for conn in list_of_clients:
                conn.close()
                print("Closed connection to " + conn)
            print("Shutdown done")
        except Exception as e:
            print("Error occurred:", str(e))
            continue

def serverloop():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    serversocket = socket.socket()
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind((ip_address,5678))
    serversocket.listen()
    while True:
        try:
            (conn, addr) = serversocket.accept()
            connected_user = conn.recv(1024).decode()
            #list_of_usernames.append(connected_user)
            #conn.send(b"test answer")
            #ack = conn.recv(1024)
            if not connected_user == "not applicable":
                user_dict[conn] = connected_user
            start_new_thread(client_thread,(conn,addr))
        except KeyboardInterrupt:
            print("Server shutdown initiated")
            for conn in list_of_clients:
                conn.close()
                print("Closed connection to " + conn)
            serversocket.close()
            print("Shutdown done")

def __user_creation(rdic,conn):
    requsername = rdic.get("username")
    reqpassword = rdic.get("password")
    reqemail = rdic.get("email")
    response={
        'type' : 'new-user',
        'status' : '',
        'message' : ''
    }
    if not lib.user_exist(requsername,db_acc) and lib.email_validator(reqemail):
        if lib.create_user(requsername, hashlib.sha256(reqpassword.encode('utf-8')).hexdigest(),reqemail,db_acc) == True:
            lib.send_signup_mail(reqemail)
            response['status'] = 'SUCCESS'
            response['message'] = 'User created'
        else:
            response['status'] = 'FAIL'
            response['message'] = 'An error occured'
    elif lib.user_exist(requsername,db_acc):
        response['status'] = 'FAIL'
        response['message'] = 'User already exists'
    elif not lib.email_validator(reqemail):
        response['status'] = 'FAIL'
        response['message'] = 'Invalid email address'

    resp_json = json.dumps(response)
    lib.transmit_message(conn, resp_json)

def __handle_login(rdic, conn):
    requsername = rdic.get("username")
    reqpassword = rdic.get("password")
    hpw=hashlib.sha256(reqpassword.encode('utf-8')).hexdigest()
    rdic = {
        "message" : "",
        "type" : ""
    }
    if lib.user_exist(requsername,db_acc) == True:
        if lib.validate_password(requsername,hpw,db_acc)==True:
            rdic["message"] = "Valid"
            rdic["type"] = lib.get_user_admin(requsername,db_acc)
        else:
            rdic["message"] = "Invalid"
            rdic["type"] = ""
    else:
        rdic["message"] = "User does not exist"
        rdic["type"] = ""
    lib.transmit_message(conn,json.dumps(rdic))


def __handle_send_message(rdic,conn):
    reqoriginator = rdic.get("current-user")
    reqreceiver = rdic.get("selected-user")
    reqbody = rdic.get("text-content")
    reqimdata = rdic.get("selected-image")
    lib.send_message(reqreceiver,reqoriginator,reqbody,user_dict,db_acc)
    
def __handle_list_request(rdic,conn):
    reqoriginator = rdic.get("current-user")
    list_of_users = lib.get_list_of_users(db_acc)
    respdict={
        'type' : 'get-user-list',
        'content' : list_of_users
    }
    jl = json.dumps(respdict)
    lib.transmit_message(conn,jl)

def __handle_get_messages(rdic,conn):
    reqoriginator = rdic.get("current-user")
    reqtarget = rdic.get("selected-user")
    message_list = lib.get_message(reqoriginator,reqtarget,db_acc)
    response={
        'type' : 'get-messages',
        'messages' : message_list
    }
    #print(message_list)
    jl = json.dumps(response)
    lib.transmit_message(conn,jl)

def __handle_delete_user(rdic,conn):
    usertodelete = rdic.get("user")
    sorf = lib.delete_user(usertodelete,db_acc)
    if sorf:
        message = {
            'type' : 'delete-user',
            'user' :  usertodelete,
            'status' : "SUCCESS"
        }
    else:
        message = {
            'type' : 'delete-user',
            'user' : usertodelete,
            'status' : "FAIL"
        }
    #print(message)
    jmsg = json.dumps(message)
    lib.transmit_message(conn,jmsg)

def __handle_generate_report(rdic,conn):
    userreport = rdic.get("user")
    report_dict = lib.get_message_report(userreport,db_acc)
    print(report_dict)
    response_dict = {
        'type' : 'report',
        'content' : report_dict
    }
    jdc = json.dumps(response_dict)
    lib.transmit_message(conn,jdc)

def request_decoder(request, conn):
    dcd = request.decode()
    rdic = json.loads(dcd)
    #print(rdic)
    reqtype = rdic.get("type")
    if reqtype=="new-user":
        __user_creation(rdic,conn)

    elif reqtype=="login":
        __handle_login(rdic,conn)

    elif reqtype=='send-message':
        __handle_send_message(rdic,conn)

    elif reqtype=='generate-report':
        __handle_generate_report(rdic,conn)
        
    elif reqtype=='delete-user':
        __handle_delete_user(rdic,conn)

    elif reqtype=='request-user-list':
        __handle_list_request(rdic,conn)

    elif reqtype=='get-messages':
        __handle_get_messages(rdic,conn)
serverloop()

