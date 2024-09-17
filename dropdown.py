from tkinter import Tk, ttk, StringVar, OptionMenu
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import filedialog

root = Tk()
root.title("Learning Python")
# root.iconbitmap("Images/Icona.ico")
root.geometry("400x400")


def show():
    global my_label
    # print(type(my_label))
    # = Label(root, text=clicked.get()).pack()
    my_label.config(text=clicked.get())


options = ["Monday",
           "Tuesday",
           "Wednesday",
           "Thursday",
           "Friday",
           "Saturday",
           "Sunday"
           ]

clicked = StringVar()
clicked.set(options[0])


drop = ttk.OptionMenu(root, clicked, options[0], *options)

drop.pack()

my_label = ttk.Label(root, text="")
my_label.pack()
# myLabel.config(text="Prova")

my_btn = ttk.Button(root, text="Show", command=show)
my_btn.pack()
# print(type(my_btn))
# Mybtn.config(text="Dai")
root.mainloop()
