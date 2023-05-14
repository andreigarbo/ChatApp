from tkinter import *
from template import Template
import json
import datetime

class Admin(Template):

    def __init__(self,current_user):
        super().__init__(current_user)
        self.root = Tk()
        self.root.title("ChatApp")
        self.root.config(bg=self.rgbtohex(53, 27, 61))
        self.root.geometry('300x400')
        self.root.resizable(0,0)
        self.current_user = current_user
        self.selected_user = 'none'

        self.user_list=Frame(self.root, width=200)
        self.user_listbox = Listbox(self.user_list)
        self.user_listbox.pack(side=LEFT, fill=BOTH)
        self.user_scrollbar=Scrollbar(self.user_list)
        self.user_scrollbar.pack(side=RIGHT, fill=BOTH)
        
        self.request_user_list()
        self.populate_listbox(self.user_listbox)

        self.user_listbox.bind("<<ListboxSelect>>", self.onselect)


        header_text=Label(self.root,text="Select user", background=self.rgbtohex(53, 27, 61), fg="white")
        header_text.grid(row=0,column=1)

        #user_picker_text=Label(root,text="Select user", bg=rgbtohex(53, 27, 61), fg="white")
        #user_picker_text.grid(row=1,column=1)

        username_field=Entry(self.root,bg="white",width=25)#change this to drop down list with all users
        self.user_list.grid(row=1,column=1,columnspan=2)

        report_button=Button(self.root,bg="white",text="Generate report",command=self.generate_report)
        report_button.grid(row=3,column=2,pady=10)

        delete_button=Button(self.root,bg="white",text="Delete user",command=self.delete_user)
        delete_button.grid(row=2,column=2,pady=10)

        logout_button=Button(self.root,bg="white",text="Log out")
        logout_button.grid(row=4,column=2,pady=10)
        
        self.selected_user_label=Label(self.root,bg=self.rgbtohex(53, 27, 61),fg='white', text="Currently selected user is " + self.selected_user)
        self.selected_user_label.grid(row=5, column=1, pady=10)

        self.root.mainloop()

    def delete_user(self):
        rdicdel = {
            "type" : "delete-user", 
            "user" : self.selected_user
        }
        request_json_del = json.dumps(rdicdel)
        self.mysocket.send(request_json_del.encode())
        self.message_ready.wait()
        #respdic = json.loads(self.message)
        print(self.message)
        #self.request_user_list()
        #self.populate_listbox(self.user_listbox)

    
    def generate_report(self):
        rdicgen = {
            "type" : 'generate-report',
            'user' : self.selected_user
        }
        request_json_generate = json.dumps(rdicgen)
        self.mysocket.send(request_json_generate.encode())
        self.message_ready.wait()
        


#admin = Admin("test-admin")