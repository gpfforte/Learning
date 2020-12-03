from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import filedialog

root=Tk()
root.title("Learning Python")
root.iconbitmap("Images/Icona.ico")


def open_w():
    global my_image
    root.filename=filedialog.askopenfilename(initialdir="images", title="Select Files", filetypes=(("jpg files","*.jpg"),("All Files","*.*")))
    my_label=Label(text=root.filename).pack()
    my_image= ImageTk.PhotoImage(Image.open(root.filename))
    my_image_label=Label(image=my_image).pack()


my_btn=Button(root, text="Open Files", command=open_w).pack()

root.mainloop()
