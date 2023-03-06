from tkinter import *

root = Tk()
root.title("ChatApp")
root.config(bg="skyblue")
root.geometry('800x300')

contact_list=Frame(root, width=200)
contact_listbox = Listbox(contact_list)
contact_listbox.pack(side=LEFT, fill=BOTH)
contact_scrollbar=Scrollbar(contact_list)
contact_scrollbar.pack(side=RIGHT, fill=BOTH)
for values in range(100):
    contact_listbox.insert(END, values)

contact_listbox.config(yscrollcommand=contact_scrollbar.set)
contact_scrollbar.config(command=contact_listbox.yview)

message_screen=Frame(root, width=100)
message_input=Text(message_screen,bg="white", height=10)
message_input.pack(side=BOTTOM)

contact_list.pack(side=LEFT)
message_screen.pack(side=RIGHT)

root.mainloop()