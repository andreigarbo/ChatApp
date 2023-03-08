import sqlite3 as sl

con = sl.connect('chatapp.db')

with con:
    con.execute("""
        CREATE TABLE user(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            hashed_password INTEGER,
            email TEXT,
            logged_on INTEGER
        );
    """)
    con.execute("""
        CREATE TABLE message(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            receiver_id INTEGER REFERENCES user(id),
            sender_id INTEGER REFERENCES user(id),
            image_content BLOB,
            text_content TEXT
        )
    """)