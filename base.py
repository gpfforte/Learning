from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import messagebox
import os

# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

root = Tk()
root.title("Learning Python")
root.iconbitmap("Images/Icona.ico")


def open_w():
    global my_img
    top = Toplevel()
    top.title("Second Window")
    top.iconbitmap("Images/Icona.ico")
    lbl = Label(top, text="Hello World").pack()
    my_img = ImageTk.PhotoImage(Image.open("images/1.jpg"))
    mylabel = Label(top, image=my_img).pack()
    btn2 = ttk.Button(top, text="Close", command=top.destroy).pack()


btn = ttk.Button(root, text="Open Window", command=open_w)
btn.pack()
# top=Toplevel()
# top.title("Second Window")
# top.iconbitmap("Images/Icona.ico")
# lbl=Label(top, text= "Hello World").pack()

# my_img=ImageTk.PhotoImage(Image.open("images/1.jpg"))
# mylabel=Label(top, image=my_img).pack()

root.mainloop()
