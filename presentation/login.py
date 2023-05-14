from tkinter import *
from template import Template
import json
from client import Client
from admin import Admin

class Login(Template):

    def __init__(self, is_admin):
        super().__init__("not applicable")
        self.root = Tk()
        self.root.title("ChatApp")
        self.root.config(bg=self.rgbtohex(53, 27, 61))
        self.root.geometry('220x140')
        self.root.resizable(0,0)
        self.response_to_login = False

        self.header_text=Label(self.root,text="Sign In", background=self.rgbtohex(53, 27, 61), fg="white")
        self.header_text.grid(row=0,column=1)

        self.username_text=Label(self.root,text="Username ", bg=self.rgbtohex(53, 27, 61), fg="white")
        self.username_text.grid(row=1,column=0)

        self.username_field=Entry(self.root,bg="white",width=25)
        self.username_field.grid(row=1,column=1,columnspan=2)

        self.password_text=Label(self.root,text="Password ", bg=self.rgbtohex(53, 27, 61), fg="white")
        self.password_text.grid(row=2,column=0)

        self.password_field=Entry(self.root,bg="white",width=25,show='*')
        self.password_field.grid(row=2,column=1,columnspan=2)

        self.login_button=Button(self.root,bg="white",text="Submit",command=self.do_login)
        self.login_button.grid(row=3,column=1, pady=10)

        self.error_label = Label(self.root, bg=self.rgbtohex(53, 27, 61), fg="red")
        self.error_label.grid(row=4, column=1)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def send_message(self):
        request_dict = {
            "type" : "login",
            "username" : self.username_field.get(),
            "password" : self.password_field.get()
        }
        request_json = json.dumps(request_dict)
        self.mysocket.send(request_json.encode())
        self.message_ready.wait()

    def do_login(self):
        self.send_message()
        dictionary = self.message
        if dictionary['message'] == "Valid" and dictionary['type']=="user":
            actvusr=self.username_field.get()
            self.on_closing() 
            client_instance = Client(actvusr)
        elif dictionary['message']=="Valid" and dictionary['type']=="admin":
            actvusr=self.username_field.get()
            self.on_closing() 
            admin_instance = Admin(actvusr)
        elif dictionary['message'] == "Invalid":
            self.error_label.config(text="Invalid credentials")
        else:
            self.error_label.config(text=self.message)

#login = Login()