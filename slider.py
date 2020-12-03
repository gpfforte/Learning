from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import filedialog

root=Tk()
root.title("Learning Python")
root.iconbitmap("Images/Icona.ico")
root.geometry("400x400")

vertical=Scale(root, from_=0, to=200)
vertical.pack()
def slide(var):
    my_label=Label(root, text=horizontal.get()).pack()
    root.geometry(str(horizontal.get())+"x400")
horizontal=Scale(root, from_=0, to=200, orient=HORIZONTAL, command=slide)
horizontal.pack()




my_btn=Button(root, text= "Click me", command=slide).pack()

root.mainloop()
