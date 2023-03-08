import re
import persistence.database_access as db

mail_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

def validate_mail(email):
    if(re.fullmatch(mail_regex, email)):
        return True
    return False

def check_if_user_exists(email,username):
    username_list = db.get_username_list()
    for username_in_db in username_list:
        if username==username_in_db:
            return True
    email_list = db.get_email_list()
    for email_in_db in email_list:
        if email==email_in_db:
            return True
    return False