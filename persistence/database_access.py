import sqlite3
import hashlib
import sys
sys.path.append('../business')
import sqlite3

class Database_access():
    def __init__(self):
        self.database = "chatapp.db"
        #self.pool = sqlite3.pool.QueuePool(lambda: sqlite3.connect(self.database), maxconnections=10)
        self.add_user_statement = 'INSERT INTO "user" (username, hashed_password, email, type, logged_on) values(?,?,?,?,?)'
        self.get_user_online_status_by_username_statement = 'SELECT logged_on FROM user WHERE username = ?'
        self.add_message_statement = 'INSERT INTO message (receiver_id, sender_id, image_content, text_content) values (?,?,?,?)'
        self.get_user_messages_statement = 'SELECT text_content FROM message WHERE receiver_id = (SELECT id FROM user WHERE username = ?) OR sender_id = (SELECT id FROM user WHERE username = ?)'
        self.get_convo_statement = 'SELECT sender_id,text_content FROM message WHERE (receiver_id = (SELECT id FROM user WHERE username = ?) AND sender_id = (SELECT id FROM user WHERE username = ?)) OR (receiver_id = (SELECT id FROM user WHERE username = ?) AND sender_id = (SELECT id FROM user WHERE username = ?))'
        self.get_report_statement = 'SELECT sender_id,receiver_id,text_content FROM message WHERE receiver_id = (SELECT id FROM user WHERE username = ?) OR sender_id = (SELECT id FROM user WHERE username = ?)'
        self.get_user_list_statement = "SELECT username FROM user WHERE type='user'"
        self.test_statement = 'SELECT text_content FROM message'
        self.get_password_by_user_statement = 'SELECT hashed_password FROM user WHERE username = ?'
        self.check_if_user_exists_statement = 'SELECT id FROM user WHERE username = ?'
        self.get_username_by_id_statement = 'SELECT username FROM user where id = ?'
        self.remove_user_statement = 'DELETE from user WHERE id = ?'
        self.get_user_or_admin_statement = 'SELECT type FROM user WHERE id = ?'
        self.count_messages_statement = 'SELECT COUNT(*) FROM message WHERE sender_id = ?'
        self.update_password_statement = 'UPDATE user SET hashed_password = ? WHERE id = ?'
        self.admin_update_password_statement = 'UPDATE user SET hashed_password = ? WHERE username = ?'
        self.get_email_by_username_statement = 'SELECT email FROM user WHERE username = ?'
        self.get_id_by_username_statement = 'SELECT id FROM user WHERE username = ?'
        self.set_logged_on_status_statement = 'UPDATE user SET logged_on = ? WHERE id = ?'
        self.get_logged_on_status_statement = 'SELECT logged_on FROM user WHERE username = ?'
        self.logout_all_users_statement = "UPDATE user SET logged_on = 'False'"
        self.is_admin_statement = "SELECT type FROM user where username = ?"

    def add_user(self,username,hashpass,email):
        with sqlite3.connect('D:/andrei/AN3/SEM2/SD/ChatApp/persistence/chatapp.db') as conn:
            conn.execute(self.add_user_statement, (username,hashpass,email,"user","False"))

    def add_message(self,fromuser,touser,message):
        #print("Adding message")
        with sqlite3.connect('D:/andrei/AN3/SEM2/SD/ChatApp/persistence/chatapp.db') as conn:
            sender_id = conn.execute("SELECT id FROM user WHERE username=?", (fromuser,)).fetchone()[0]
            receiver_id = conn.execute("SELECT id FROM user WHERE username=?", (touser,)).fetchone()[0]
            image_content = None
            message_tuple = (receiver_id, sender_id, image_content, message)
            conn.execute(self.add_message_statement, message_tuple)

    def get_user_messages(self,fromuser, touser):
        with sqlite3.connect('D:/andrei/AN3/SEM2/SD/ChatApp/persistence/chatapp.db') as conn:
            messages=conn.execute(self.get_convo_statement, (fromuser, touser, touser, fromuser)).fetchall()
            return [(self.get_username_by_id(message[0]),message[1]) for message in messages]
        
    def get_username_by_id(self,id):
        with sqlite3.connect('D:/andrei/AN3/SEM2/SD/ChatApp/persistence/chatapp.db') as conn:
            return conn.execute(self.get_username_by_id_statement,(id,)).fetchone()[0]
             
    def test(self):
        with sqlite3.connect('D:/andrei/AN3/SEM2/SD/ChatApp/persistence/chatapp.db') as conn:
            return conn.execute(self.test_statement).fetchall()

    def get_user_list(self):
        with sqlite3.connect('D:/andrei/AN3/SEM2/SD/ChatApp/persistence/chatapp.db') as conn:
            return [row[0] for row in conn.execute(self.get_user_list_statement).fetchall()]

    def get_password_by_user(self,username):
        with sqlite3.connect('D:/andrei/AN3/SEM2/SD/ChatApp/persistence/chatapp.db') as conn:
            result = conn.execute(self.get_password_by_user_statement, (username,)).fetchone()
            if result is not None:
                hashed_password = result[0]
                return hashed_password
        return None

    def check_if_user_exists(self,username):
        with sqlite3.connect('D:/andrei/AN3/SEM2/SD/ChatApp/persistence/chatapp.db') as conn:
            result = conn.execute(self.check_if_user_exists_statement, (username,)).fetchone()
            if result:
                return True

            return False
        
    def get_convo(self,fromuser,touser):
        with sqlite3.connect('D:/andrei/AN3/SEM2/SD/ChatApp/persistence/chatapp.db') as conn:
            return [row[0] for row in conn.execute(self.get_convo_statement, (fromuser,touser,touser,fromuser)).fetchall()]
        
    def remove_user_from_database(self,delete):
        print("PARAM")
        print(delete)
        with sqlite3.connect('D:/andrei/AN3/SEM2/SD/ChatApp/persistence/chatapp.db') as conn:
            getid = conn.execute("SELECT id FROM user WHERE username=?", (delete,)).fetchone()[0]
            conn.execute(self.remove_user_statement, (getid,))
            if self.check_if_user_exists(delete):
                return False
            return True

    def get_user_or_admin(self,username):
        with sqlite3.connect('D:/andrei/AN3/SEM2/SD/ChatApp/persistence/chatapp.db') as conn:
            getid = conn.execute("SELECT id FROM user WHERE username=?", (username,)).fetchone()[0]
            return conn.execute(self.get_user_or_admin_statement,(getid,)).fetchone()[0]
        
    def get_messages_report(self,username):
        with sqlite3.connect('D:/andrei/AN3/SEM2/SD/ChatApp/persistence/chatapp.db') as conn:
            cursor = conn.execute(self.get_report_statement, (username, username))
            rows = cursor.fetchall()
            report_dict = {
                'sender': [],
                'receiver': [],
                'text_content': []
            }
            for row in rows:
                sender_username = self.get_username_by_id(row[0])
                receiver_username = self.get_username_by_id(row[1])
                report_dict['sender'].append(sender_username)
                report_dict['receiver'].append(receiver_username)
                report_dict['text_content'].append(row[2])
            return report_dict
        
    def count_sender_messages(self, username):
        with sqlite3.connect('D:/andrei/AN3/SEM2/SD/ChatApp/persistence/chatapp.db') as conn:
            id = conn.execute("SELECT id FROM user WHERE username=?", (username,)).fetchone()[0]
            return conn.execute(self.count_messages_statement, (id,)).fetchone()[0]
        
    def update_password(self,username,old,new):
        status = 'FAIL'
        with sqlite3.connect('D:/andrei/AN3/SEM2/SD/ChatApp/persistence/chatapp.db') as conn:
            id = conn.execute("SELECT id FROM user WHERE username=?", (username,)).fetchone()[0]
            pfdb = conn.execute(self.get_password_by_user_statement,(username,)).fetchone()[0]
            if old == pfdb:
                conn.execute(self.update_password_statement,(new, id))
                status = 'SUCCESS'
        return status
    
    def get_email_by_username(self, username):
        with sqlite3.connect('D:/andrei/AN3/SEM2/SD/ChatApp/persistence/chatapp.db') as conn:
            return conn.execute(self.get_email_by_username_statement,(username,)).fetchone()[0]
        
    def get_id_by_username(self, username):
        with sqlite3.connect('D:/andrei/AN3/SEM2/SD/ChatApp/persistence/chatapp.db') as conn:
            id=conn.execute(self.get_id_by_username_statement,(username,)).fetchone()[0]
            return id
        
    def set_logged_on_status(self, username, status):
        with sqlite3.connect('D:/andrei/AN3/SEM2/SD/ChatApp/persistence/chatapp.db') as conn:
            id=self.get_id_by_username(username)
            #print("setting status for user " + username + " with id " + id + " to " + status)
            conn.execute(self.set_logged_on_status_statement, (status,id))
        
    def get_logged_on_status(self,username):
        with sqlite3.connect('D:/andrei/AN3/SEM2/SD/ChatApp/persistence/chatapp.db') as conn:
            return conn.execute(self.get_logged_on_status_statement, (username,)).fetchone()[0]
        
    def logout_all_users(self):
        with sqlite3.connect('D:/andrei/AN3/SEM2/SD/ChatApp/persistence/chatapp.db') as conn:
            conn.execute(self.logout_all_users_statement)


    def is_admin(self,username):
        with sqlite3.connect('D:/andrei/AN3/SEM2/SD/ChatApp/persistence/chatapp.db') as conn:
            type = conn.execute(self.is_admin_statement, (username,)).fetchone()[0]
            if type == 'admin':
                return True
        return False
    
    def admin_change_password(self,username,password):
        with sqlite3.connect('D:/andrei/AN3/SEM2/SD/ChatApp/persistence/chatapp.db') as conn:
            #conn.execute(self.admin_update_password_statement, (password,username))
            print(username + " " +  password)
            status = conn.execute(self.admin_update_password_statement, (password,username))
            print(status)
            if status == 0:
                return False
        return True
            