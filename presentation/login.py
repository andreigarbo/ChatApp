from tkinter import *
import business.request_handler as req
import business.models as ms

def rgbtohex(r,g,b):
    return f'#{r:02x}{g:02x}{b:02x}'

root = Tk()
root.title("ChatApp")
root.config(bg=rgbtohex(53, 27, 61))
root.geometry('220x120')
root.resizable(0,0)

header_text=Label(root,text="Sign In", background=rgbtohex(53, 27, 61), fg="white")
header_text.grid(row=0,column=1)

username_text=Label(root,text="Username ", bg=rgbtohex(53, 27, 61), fg="white")
username_text.grid(row=1,column=0)

username_field=Entry(root,bg="white",width=25)
username_field.grid(row=1,column=1,columnspan=2)

password_text=Label(root,text="Password ", bg=rgbtohex(53, 27, 61), fg="white")
password_text.grid(row=2,column=0)

password_field=Entry(root,bg="white",width=25,show='*')
password_field.grid(row=2,column=1,columnspan=2)

login_button=Button(root,bg="white",text="Submit",command=lambda : req.request_decoder(ms.request('login', [username_field.get(), password_field.get()])))
login_button.grid(row=3,column=1, pady=10)

root.mainloop()