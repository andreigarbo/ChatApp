import sqlite3 as sl

con = sl.connect('chatapp.db')

add_user_statement = 'INSERT INTO user (username, hashed_password, email, logged_on) values(?,?,?,?)'
get_user_online_status_by_username_statement = 'SELECT logged_on FROM user WHERE username = ?'
add_message_statement = 'INSERT INTO message (receiver_id, sender_id, image_content, text_content) values (?,?,?,?)'
get_user_messages_statement = 'SELECT * FROM message WHERE receiver_id = (SELECT username FROM user WHERE id = receiver_id) OR receiver_id = (SELECT username FROM user WHERE id = sender_id)'
get_username_list_statement = 'SELECT username FROM user'

def add_user(user):
    with con:
        con.executemany(add_user_statement, user)

def add_message(message):
    with con:
        con.executemany(add_message_statement, message)

def get_user_messages(user):
    with con:
        return con.executemany(get_user_messages_statement, user)
    
def get_username_list():
    with con:
        return con.executemany(get_username_list_statement)

def get_user_online_status_by_username(username):
    with con:
        return con.execute(get_user_online_status_by_username_statement, username)