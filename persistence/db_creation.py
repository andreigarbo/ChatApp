import sqlite3 as sl
import hashlib

con = sl.connect('chatapp.db')

with con:
    #con.execute("""
    #    CREATE TABLE user(
    #        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    #        username TEXT,
    #        hashed_password TEXT,
    #        email TEXT,
    #        type TEXT,
    #        logged_on TEXT
    #    );
    #""")
    #con.execute("""
    #    CREATE TABLE message(
    #        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    #        receiver_id INTEGER REFERENCES user(id),
    #        sender_id INTEGER REFERENCES user(id),
    #        image_content BLOB,
    #        text_content TEXT
    #    )
    #""")
    #con.execute('INSERT INTO "user" (username, hashed_password, email, type, logged_on) values(?,?,?,?,?)',("user1",hashlib.sha256("user1".encode('utf-8')).hexdigest(),"user1@email.com","user","false"))
    #con.execute('INSERT INTO "user" (username, hashed_password, email, type, logged_on) values(?,?,?,?,?)',("user2",hashlib.sha256("user2".encode('utf-8')).hexdigest(),"user2@email.com","user","false"))
    #con.execute('INSERT INTO "user" (username, hashed_password, email, type, logged_on) values(?,?,?,?,?)',("user3",hashlib.sha256("user3".encode('utf-8')).hexdigest(),"user3@email.com","user","false"))
    #con.execute('INSERT INTO "user" (username, hashed_password, email, type, logged_on) values(?,?,?,?,?)',("user4",hashlib.sha256("user4".encode('utf-8')).hexdigest(),"user4@email.com","user","false"))
    #con.execute('DELETE FROM message')
    con.execute("DELETE FROM user WHERE username='test_mail'")
    #con.execute('INSERT INTO message (receiver_id, sender_id, image_content, text_content) values (?,?,?,?)')
    #con.execute('INSERT INTO "user" (username, hashed_password, email, type, logged_on) values(?,?,?,?,?)',("admin",hashlib.sha256("admin".encode('utf-8')).hexdigest(),"admin@admin.com","admin","false"))