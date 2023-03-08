import models as ms
import hashlib as hs
import persistence.database_access

def user_creation(username,password,email):
    created_user=ms.user(username,hs.sha256(password),email)
    persistence.database_access.add_user(created_user)

def request_decoder(request):

    if request=="create-new-user":
        user_creation(request.username,request.password,request.email)
    
        