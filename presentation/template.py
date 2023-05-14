import socket
import json
import select
import tkinter as tk
import threading

class Template():

    def __init__(self, username):
        self.current_user = username
        self.host = socket.gethostname()
        self.port = 5678
        self.mysocket = socket.socket()
        self.mysocket.connect((self.host, self.port))
        self.mysocket.send(username.encode())
        self.receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        self.receive_thread.start()
        self.message = ''
        self.message_ready = threading.Event()
        self.message_dict = {}
        self.selected_user = 'none'
    
    def rgbtohex(self, r,g,b):
            return f'#{r:02x}{g:02x}{b:02x}'

    def on_closing(self):
        self.mysocket.send("DISCONNECT".encode())
        self.mysocket.shutdown(socket.SHUT_RDWR)
        self.mysocket.close()
        try:
            self.scheduler_thread.stop()
        except:
            pass
        self.root.destroy()
    
    def send_message(self):
        pass

    def receive_messages(self):
        connection_closed = False
        while not connection_closed:
            try:
                read_sockets, _, _ = select.select([self.mysocket], [], [])
                for socks in read_sockets:
                    self.message = socks.recv(1024)
                    if self.message:
                        self.message = self.message.decode()
                        self.message = json.loads(self.message)
                        if(self.message['type'] == 'ask-for-messages'):
                            print("server asked me to refresh the messages")
                            socks.send(b"ACK")
                            self.refresh_messages()

                        else:
                            self.message_ready.set()
            except (OSError, ConnectionResetError):
                connection_closed = True
                break

    def request_user_list(self):
        request_dict = {
            "type" : "request-user-list",
            "current-user" : self.current_user
        }
        request_json = json.dumps(request_dict)
        self.mysocket.send(request_json.encode())
        self.message_ready.wait()

    def populate_listbox(self, listbox):

        listbox.delete(0,'end')
        #print("SELF MESSAGE " + self.message)
        #ulist = json.loads(self.message)
        for u in self.message['content']:
            listbox.insert(tk.END,u)

    def onselect(self,evt):
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        self.selected_user = value
        self.selected_user_label.config(text="Currently selected user is " + self.selected_user)


