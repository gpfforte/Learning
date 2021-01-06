from tkinter import *


root=Tk()
root.title("Learning Python")
root.geometry("400x400")

options=["Lun", "Mar", "Mer"]


clicked=StringVar()
clicked.set(options[0])
def stampa(event):
    print(clicked.get())
# Nella prossima riga l'asterisco serve per spacchettare la lista passata come argomento
dropmenu=OptionMenu(root, clicked, *options, command=stampa)
dropmenu.pack()


root.mainloop()
