from tkinter import *
from tkinter import filedialog as fd
import business.models as ms
import json
from template import Template
from apscheduler.schedulers.background import BlockingScheduler
import threading

class Client(Template):

    def __init__(self, current_user):
        super().__init__(current_user)
        self.current_user = current_user
        self.selected_image_path = "none"
        self.selected_image = ''
        
        self.root = Tk()
        self.root.title("ChatApp")
        self.root.config(bg=self.rgbtohex(53, 27, 61))
        #self.root.geometry('743x370')
        self.root.resizable(0,0)

        self.contact_list=Frame(self.root, width=200)
        self.contact_listbox = Listbox(self.contact_list)
        self.contact_listbox.pack(side=LEFT, fill=BOTH)
        self.contact_scrollbar=Scrollbar(self.contact_list)
        self.contact_scrollbar.pack(side=RIGHT, fill=BOTH)

        self.request_user_list()
        #
        #print(self.message)
        self.populate_listbox(self.contact_listbox)

        self.contact_listbox.bind("<<ListboxSelect>>", self.onselect2)

        self.contact_listbox.config(yscrollcommand=self.contact_scrollbar.set)
        self.contact_scrollbar.config(command=self.contact_listbox.yview)
        self.contact_list.grid(row=0,column=0,sticky='ns',rowspan=2)

        self.message_screen=Frame(self.root,bg="white", height=100,width=100)
        self.message_screen.grid(row=0,column=1,stick='e')

        self.message_display=Text(self.message_screen, bg="white", wrap=WORD, state=DISABLED)
        self.message_display.pack(fill=BOTH, expand=YES)

        self.message_input=Entry(self.root,bg="white",width=100)
        self.message_input.grid(row=1,column=1, sticky='e')

        self.send_button=Button(self.root, bg="white",text="Send", command=self.send_message)
        self.send_button.grid(row=2,column=1,sticky='e')

        self.send_file=Button(self.root, bg="white", text="Select & send file")
        self.send_file.grid(row=3, column=1, sticky='e')

        self.selected_user_label=Label(self.root,bg=self.rgbtohex(53, 27, 61),fg='white', text="Currently selected user is " + self.selected_user)
        self.selected_user_label.grid(row=4, column=1, sticky='e')

        self.current_user_label=Label(self.root,bg=self.rgbtohex(53, 27, 61),fg='white', text="Currently logged as " + self.current_user)
        self.current_user_label.grid(row=4, column=0, sticky='e')

        self.root.update_idletasks()
        self.root.geometry(str(self.root.winfo_width()) + "x" + str(self.root.winfo_height()))

        #self.scheduler = BlockingScheduler()
        #self.scheduler.add_job(self.refresh_messages, 'interval', seconds=1)
        #self.scheduler.start()

        self.scheduler_thread = threading.Thread(target=self.refresh_messages_periodically)
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def refresh_messages_periodically(self):
        scheduler = BlockingScheduler()
        scheduler.add_job(self.refresh_messages, 'interval', seconds=0.5)
        scheduler.start()

    def refresh_messages(self):
        if self.selected_user != "none":
            self.message_display.config(state=NORMAL)
            request_dict = {
                "type" : "get-messages",
                "current-user" : self.current_user,
                "selected-user" : self.selected_user,
            }
            request_json = json.dumps(request_dict)
            self.mysocket.send(request_json.encode())
            self.message_ready.wait()
            #messages = json.loads(self.message)
            if 'messages' in self.message:
                #print("messages field exists")
                self.update_message_display(self.message['messages'])

    def onselect2(self,evt):
        self.onselect(evt)
        self.refresh_messages()
        self.refresh_messages()
        self.refresh_messages()
        self.refresh_messages()
        self.refresh_messages()


    def send_message(self):
        #print("SENDING MESSAGE")
        request_dict = {
            "type" : "send-message",
            "current-user" : self.current_user,
            "selected-user" : self.selected_user,
            "text-content" : self.message_input.get(),
            "selected-image" : self.selected_image
        }
        request_json = json.dumps(request_dict)
        #print(request_json)
        self.mysocket.send(request_json.encode())
        self.refresh_messages()
        self.refresh_messages()
        self.refresh_messages()
        self.refresh_messages()
        self.refresh_messages()

    def update_message_display(self, messages):  
        self.message_display.config(state=NORMAL)      
        self.message_display.delete("1.0", "end")
        for message in messages:
            self.message_display.insert(END, f"{message[0]}: {message[1]}\n")
        self.message_display.config(state=DISABLED)
        self.message_display.update_idletasks()
 
    def update_selected_user(self,event):
        #print("SELECTING USER " + self.contact_listbox.get(ACTIVE))
        if(self.contact_listbox.get(ACTIVE) != ''):
            self.selected_user = self.contact_listbox.get(ACTIVE)
            self.refresh_messages()
        self.selected_user_label.config(text="Currently selected user is " + self.selected_user)

#client = Client("test_user")