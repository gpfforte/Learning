from tkinter import *
root=Tk()

def Myclick():
    Mylabel=Label(root, text="Ho premuto un tasto")
    Mylabel.pack()

myButton=Button(root, text="Premi qui!", padx=50, pady=50, command=Myclick, fg="blue", bg="red")
myButton.pack()

root.mainloop()
