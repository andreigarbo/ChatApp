
class user:
    def __init__(self, username, hashed_password):
        self.username = username
        self.hashed_password = hashed_password
        self.logged_on = False

class message:
    def __init__(self, receiver_id, sender_id, image_content, text_content):
        self.receiver_id = receiver_id
        self.sender_id = sender_id
        self.image_content = image_content
        self.text_content = text_content