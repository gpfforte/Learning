from tkinter import *


root=Tk()
root.title("Learning Python")
root.geometry("400x400")

my_menu = Menu(root)
root.config(menu=my_menu)

def file_new():
    hide_all_frames()
    file_new_frame.pack(fill="both", expand=1)
    my_label=Label(file_new_frame, text="You Clicked file new")
    my_label.pack()

def paste():
    pass

def cut():
    hide_all_frames()
    edit_cut_frame.pack(fill="both", expand=1)
    my_label=Label(edit_cut_frame, text="You Clicked edit cut")
    my_label.pack()

def hide_all_frames():
    file_new_frame.pack_forget()
    edit_cut_frame.pack_forget()


file_menu=Menu(my_menu)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New...", command=file_new)
file_menu.add_separator()
file_menu.add_command(label="Quit", command=root.destroy)


edit_menu=Menu(my_menu)
my_menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut", command=cut)
edit_menu.add_separator()
edit_menu.add_command(label="Copy", command=paste)

file_new_frame=Frame(root, width=400, height=400, bg="red")
edit_cut_frame=Frame(root, width=400, height=400, bg="blue")

root.mainloop()