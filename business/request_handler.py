import business.models as ms
import hashlib as hs
import persistence.database_access
import business.validators as vd
from PIL import ImageTk, Image

def __user_creation(username,password,email):
    #if(vd.check_if_user_exists(email,username)==False):
    created_user=ms.user(username,hs.sha256(password.encode('utf-8')),email)
    persistence.database_access.add_user(created_user)
    #else:
        #print("USER ALREADY EXISTS")

def request_decoder(request : ms.request):

    if request.type=="new-user":
        #__user_creation(request.username,request.password,request.email)
        print("new user requested")
        print(request.type)
        print(request.body)
    elif request.type=="login":
        print("login")
        print(request.type)
        print(request.body)
    elif request.type=='send-message':
        print("send message")
        print(request.type)
        print(request.body)
        image = request.body[3]
        image.show()
    
#__user_creation('admin','admin','admin@admin.com')
    
