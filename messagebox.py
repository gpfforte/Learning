from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox

root=Tk()
root.title("Learning Python")
root.iconbitmap("Images/Icona.ico")

# showinfo(): Show some relevant information to the user.
# showwarning(): Display the warning to the user.
# showerror(): Display the error message to the user.
# askquestion(): Ask question and user has to answered in yes or no.
# askokcancel(): Confirm the user’s action regarding some application activity.
# askyesno(): User can answer in yes or no for some action.
# askretrycancel(): Ask the user about doing a particular task again or not.

def popup():
    response=messagebox.askokcancel("This is my popup","Hello World")
    Label(root, text=response).pack()
    # if response==1:
    #     Label(root, text="You Clicked Yes").pack()
    # else:
    #     Label(root, text="You Clicked No").pack()
Button(root, text="Popup", command=popup).pack()


# button_quit=Button(root, text="Quit Program", command=root.destroy)
# button_quit.grid(row=1, column=1)

root.mainloop()
