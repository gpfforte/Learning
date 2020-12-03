from tkinter import *
from PIL import ImageTk, Image


root=Tk()
root.title("Learning Python")
root.iconbitmap("Images/Icona.ico")

# r=IntVar()
# r.set("2")
#r=StrVar()

MODES=[
    ("Pepperoni","Pepperoni"),
    ("Cheese","Cheese"),
    ("Mushroom","Mushroom"),
    ("Onion","Onion"),
]

pizza= StringVar()
pizza.set("Pepperoni")

for text, mode in MODES:
    Radiobutton(root,text=text, variable= pizza, value=mode).pack(anchor=W)

def clicked(value):
    myLabel=Label(root, text=value)
    myLabel.pack()

# Radiobutton(root, text="Option 1", variable=r,value=1, command= lambda: clicked(r.get())).pack()
# Radiobutton(root, text="Option 2", variable=r,value=2, command= lambda: clicked(r.get())).pack()
# Radiobutton(root, text="Option 1", variable=r,value=1).pack()
# Radiobutton(root, text="Option 2", variable=r,value=2).pack()
# myLabel=Label(root, text=pizza.get())
# myLabel.pack()


myButton=Button(root, text= "Click me!", command=lambda: clicked(pizza.get()))
myButton.pack()

# button_quit=Button(root, text="Quit Program", command=root.destroy)
# button_quit.grid(row=1, column=1)

root.mainloop()
