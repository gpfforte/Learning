from tkinter import *
root=Tk()

def Myclick():
    Mylabel=Label(root, text=Myinput.get())
    Mylabel.pack()
    Myinput.insert(0,"C")

Myinput=Entry(root, width=50, bg="red", fg="#ffffff", borderwidth=5)
Myinput.pack()
Myinput.insert(0,"Digita quello che vuoi")

myButton=Button(root, text="Premi qui!", padx=50, pady=50, command=Myclick, fg="blue", bg="red")
myButton.pack()

root.mainloop()
