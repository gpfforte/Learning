from tkinter import *
from PIL import ImageTk, Image


root=Tk()
root.title("Learning Python")
root.iconbitmap("Images/Icona.ico")

my_frame = LabelFrame(root, text= "Frame...", padx=50, pady=50)
my_frame.pack(padx=10, pady=10)

button_1=Button(my_frame, text="Button in a Frame")
button_2=Button(my_frame, text="2Button in a Frame")
button_1.grid(row=0,column=0)
button_2.grid(row=1,column=1)

# button_quit=Button(root, text="Quit Program", command=root.destroy)
# button_quit.grid(row=1, column=1)

root.mainloop()
