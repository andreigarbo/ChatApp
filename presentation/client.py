from tkinter import *
from tkinter import filedialog as fd
from PIL import ImageTk, Image
import business.request_handler as req
import business.models as ms

def rgbtohex(r,g,b):
    return f'#{r:02x}{g:02x}{b:02x}'

root = Tk()
root.title("ChatApp")
root.config(bg=rgbtohex(53, 27, 61))
root.geometry('743x370')
root.resizable(0,0)

#root.rowconfigure(0, weight=3)

current_user = "admin_test"
global selected_image_path
global selected_image
selected_image_path="none"
selected_image=''

def __select_image():
    global selected_image_path
    global selected_image
    selected_image_path = fd.askopenfilename(initialdir="/Pictures", title="Select file to send")
    selected_image = Image.open(selected_image_path)
    #selected_image.show()

contact_list=Frame(root, width=200)
contact_listbox = Listbox(contact_list)
contact_listbox.pack(side=LEFT, fill=BOTH)
contact_scrollbar=Scrollbar(contact_list)
contact_scrollbar.pack(side=RIGHT, fill=BOTH)
for values in range(100):
    contact_listbox.insert(END, "test")

contact_listbox.config(yscrollcommand=contact_scrollbar.set)
contact_scrollbar.config(command=contact_listbox.yview)
contact_list.grid(row=0,column=0,sticky='ns',rowspan=2)

message_screen=Frame(root,bg="white", height=300)
message_screen.grid(row=0,column=1,stick='e')

message_input=Entry(root,bg="white",width=100)
message_input.grid(row=1,column=1, sticky='e')

send_button=Button(root, bg="white",text="Send",command=lambda : req.request_decoder(ms.request('send-message', [current_user, contact_listbox.get(ACTIVE), message_input.get(),selected_image])))
send_button.grid(row=2,column=1,sticky='e')

send_file=Button(root, bg="white", text="Select & send file",command= lambda: __select_image())
send_file.grid(row=3, column=1, sticky='e')

root.mainloop()