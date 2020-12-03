from tkinter import *
from PIL import ImageTk, Image


root=Tk()
root.title("Learning Python")
root.iconbitmap("Images/Icona.ico")

my_img_1=ImageTk.PhotoImage(Image.open("Images/1.jpg"))
my_img_2=ImageTk.PhotoImage(Image.open("Images/2.jpg"))
my_img_3=ImageTk.PhotoImage(Image.open("Images/3.jpg"))
my_img_4=ImageTk.PhotoImage(Image.open("Images/4.jpg"))
my_img_5=ImageTk.PhotoImage(Image.open("Images/5.jpg"))

my_image_list = [my_img_1,my_img_2,my_img_3,my_img_4,my_img_5]

status=Label(root,text="Image 1 of "+str(len(my_image_list)), bd=1,relief=SUNKEN, anchor=W)

my_label=Label(image=my_img_1)
my_label.grid(row=0, column=0, columnspan=3)

image_number=0

def forw(image_n):
    global my_label
    my_label.grid_forget()
    my_label=Label(image=my_image_list[image_n])
    my_label.grid(row=0, column=0, columnspan=3)
    global image_number
    global button_forw
    if (image_n == 4):
        button_forw['state'] = DISABLED
    button_back['state'] = NORMAL
    image_number=image_n
    status=Label(root,text="Image "+ str(image_number+1)+" of "+str(len(my_image_list)), bd=1,relief=SUNKEN, anchor=W)
    status.grid(row=2, column=0, columnspan=3,sticky=W+E)
    
def back(image_n):
    global my_label
    my_label.grid_forget()
    my_label=Label(image=my_image_list[image_n])
    my_label.grid(row=0, column=0, columnspan=3)
    global image_number
    global button_back
    if (image_n == 0):
        button_back['state'] = DISABLED
    button_forw['state'] = NORMAL
    image_number=image_n
    status=Label(root,text="Image "+ str(image_number+1)+" of "+str(len(my_image_list)), bd=1,relief=SUNKEN, anchor=W)
    status.grid(row=2, column=0, columnspan=3,sticky=W+E)

button_forw=Button(root, text=">>", command=lambda: forw(image_number + 1))
button_back=Button(root, text="<<", command=lambda: back(image_number - 1))

button_forw.grid(row=1, column=2, pady=10)
button_back.grid(row=1, column=0)

status.grid(row=2, column=0, columnspan=3,sticky=W+E)



button_quit=Button(root, text="Quit Program", command=root.destroy)
button_quit.grid(row=1, column=1)

root.mainloop()
