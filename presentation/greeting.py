from tkinter import *
from login import Login
from user_creation import User_creation

class Greeting():

    def __init__(self):
        self.root = Tk()
        self.root.title("ChatApp")
        self.root.config(bg=self.rgbtohex(53, 27, 61))
        self.root.geometry('140x130')
        self.root.resizable(0,0)

        self.header_text=Label(self.root,text="Welcome to ChatApp", background=self.rgbtohex(53, 27, 61), fg="white")
        self.header_text.grid(row=0,column=1)

        self.login_button=Button(self.root,bg="white",text="Login",command=self.open_login)
        self.login_button.grid(row=1,column=1, pady=10)

        self.create_account_button=Button(self.root,bg="white",text="Create Account", command=self.open_user_creation)
        self.create_account_button.grid(row=2,column=1, pady=10)

        self.root.protocol("WM_DELETE_WINDOW")
        self.root.mainloop()

    def open_login(self):
        #self.root.destroy()
        login_window = Login(False)

    def open_user_creation(self):
        #self.root.destroy()
        user_creation_window = User_creation()

    def rgbtohex(self, r,g,b):
        return f'#{r:02x}{g:02x}{b:02x}'

greeting = Greeting()