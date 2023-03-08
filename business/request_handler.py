import models as ms
import hashlib as hs
import persistence.database_access
import validators as vd

def user_creation(username,password,email):
    #if(vd.check_if_user_exists(email,username)==False):
    created_user=ms.user(username,hs.sha256(password.encode('utf-8')),email)
    persistence.database_access.add_user(created_user)
    #else:
        #print("USER ALREADY EXISTS")

def request_decoder(request):

    if request=="create-new-user":
        user_creation(request.username,request.password,request.email)
    
user_creation('admin','admin','admin@admin.com')
    
