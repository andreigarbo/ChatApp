from tkinter import *
import json
from template import Template

class User_creation(Template):
        
    def __init__(self):
        super().__init__("not applicable")
        self.root = Tk()
        self.root.title("ChatApp")
        self.root.config(bg=self.rgbtohex(53, 27, 61))
        self.root.geometry('250x180')
        self.root.resizable(0,0)

        self.header_text=Label(self.root,text="Sign Up", background=self.rgbtohex(53, 27, 61), fg="white")
        self.header_text.grid(row=0,column=1)

        self.username_text=Label(self.root,text="Username ", bg=self.rgbtohex(53, 27, 61), fg="white")
        self.username_text.grid(row=1,column=0)

        self.username_field=Entry(self.root,bg="white",width=30)
        self.username_field.grid(row=1,column=1,columnspan=2)

        self.password_text=Label(self.root,text="Password ", bg=self.rgbtohex(53, 27, 61), fg="white")
        self.password_text.grid(row=2,column=0)

        self.password_field=Entry(self.root,bg="white",width=30,show='*')
        self.password_field.grid(row=2,column=1,columnspan=2)

        self.email_text=Label(self.root,text="EMail ", bg=self.rgbtohex(53, 27, 61), fg="white")
        self.email_text.grid(row=3,column=0)

        self.email_field=Entry(self.root,bg="white", width=30)
        self.email_field.grid(row=3,column=1,columnspan=2)

        self.create_account_button=Button(self.root,bg="white",text="Create account", command=self.do_create)
        self.create_account_button.grid(row=4,column=1, pady=10)

        self.info_label = Label(self.root, bg=self.rgbtohex(53, 27, 61), fg="red")
        self.info_label.grid(row=5, column=1)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    
    def send_message(self):
        request_dict = {
            "type" : "new-user",
            "username" : self.username_field.get(),
            "password" : self.password_field.get(),
            "email" : self.email_field.get()
        }
        request_json = json.dumps(request_dict)
        self.mysocket.send(request_json.encode())

    def do_create(self):
        self.send_message()
        self.message_ready.wait()
        respdic = self.message
        self.info_label.config(text=self.message['message']) 

#user_creation = User_creation()