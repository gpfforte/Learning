from tkinter import *


root=Tk()
root.title("Learning Python")
root.geometry("400x400")

my_menu = Menu(root)
root.config(menu=my_menu)

def file_new():
    pass

def paste():
    pass

def cut():
    pass

file_menu=Menu(my_menu)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New...", command=file_new)
file_menu.add_separator()
file_menu.add_command(label="Quit", command=root.destroy)


edit_menu=Menu(my_menu)
my_menu.add_cascade(label="Copy", menu=edit_menu)
edit_menu.add_command(label="Cut", command=cut)
edit_menu.add_separator()
edit_menu.add_command(label="Copy", command=paste)

root.mainloop()