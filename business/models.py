
class user:
    def __init__(self, username, hashed_password,email):
        self.username = username
        self.hashed_password = hashed_password
        self.email=email
        self.logged_on = False

class message:
    def __init__(self, receiver_id, sender_id, image_content, text_content):
        self.receiver_id = receiver_id
        self.sender_id = sender_id
        self.image_content = image_content
        self.text_content = text_content

class request:
    def __init__(self, type : str, body : list):
        self.type = type
        self.body = body
        