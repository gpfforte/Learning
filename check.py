from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import filedialog

root = Tk()
root.title("Learning Python")
# root.iconbitmap("Images/Icona.ico")
root.geometry("400x400")


def show():
    myLabel = Label(root, text=var.get()).pack()


#var= IntVar()
var = StringVar()
c = ttk.Checkbutton(root, text="Check this box", variable=var,
                    onvalue="Pizza", offvalue="Hamburger")
c.selection_clear()
c.pack()


Mybutton = ttk.Button(root, text="Show Selection", command=show).pack()

root.mainloop()
