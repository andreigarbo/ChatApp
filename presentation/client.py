from tkinter import *

def rgbtohex(r,g,b):
    return f'#{r:02x}{g:02x}{b:02x}'

root = Tk()
root.title("ChatApp")
root.config(bg=rgbtohex(53, 27, 61))
root.geometry('743x345')
root.resizable(0,0)

#root.rowconfigure(0, weight=3)

contact_list=Frame(root, width=200)
contact_listbox = Listbox(contact_list)
contact_listbox.pack(side=LEFT, fill=BOTH)
contact_scrollbar=Scrollbar(contact_list)
contact_scrollbar.pack(side=RIGHT, fill=BOTH)
for values in range(100):
    contact_listbox.insert(END, values)

contact_listbox.config(yscrollcommand=contact_scrollbar.set)
contact_scrollbar.config(command=contact_listbox.yview)
contact_list.grid(row=0,column=0,sticky='ns',rowspan=2)

message_screen=Frame(root,bg="white", height=300)
message_screen.grid(row=0,column=1,stick='e')

message_input=Entry(root,bg="white",width=100)
message_input.grid(row=1,column=1, sticky='e')


send_button=Button(root, bg="white",text="Send")
send_button.grid(row=2,column=1,sticky='e')



root.mainloop()