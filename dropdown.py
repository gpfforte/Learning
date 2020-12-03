from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import filedialog

root=Tk()
root.title("Learning Python")
root.iconbitmap("Images/Icona.ico")
root.geometry("400x400")

def show():
	myLabel=Label(root, text=clicked.get()).pack()

options=["Monday",
	"Tuesday",
	"Wednesday",
	"Thuday",
	"Friday",
	"Saturday",
	"Sunday"
]

clicked=StringVar()
clicked.set(options[0])



drop=OptionMenu(root, clicked, *options)
drop.pack()


Mybtn=Button(root, text="Show", command=show).pack()
root.mainloop()
