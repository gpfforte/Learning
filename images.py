from tkinter import *
from PIL import ImageTk, Image


root=Tk()
root.title("Learning Python")
root.iconbitmap("C:/Users/forteg/Desktop/Python/Icona.ico")

my_img_1=ImageTk.PhotoImage(Image.open("C:/Users/forteg/Desktop/Python/1.jpg"))
my_img_2=ImageTk.PhotoImage(Image.open("C:/Users/forteg/Desktop/Python/2.jpg"))
my_img_3=ImageTk.PhotoImage(Image.open("C:/Users/forteg/Desktop/Python/3.jpg"))

my_image_list = [my_img_1,my_img_2,my_img_3]

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
    if (image_n == 2):
        button_forw['state'] = DISABLED
    button_back['state'] = NORMAL
    image_number=image_n
    
    
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

button_forw=Button(root, text=">>", command=lambda: forw(image_number + 1))
button_back=Button(root, text="<<", command=lambda: back(image_number - 1))

button_forw.grid(row=1, column=2)
button_back.grid(row=1, column=0)
"""

"""




button_quit=Button(root, text="Quit Program", command=root.quit)
button_quit.grid(row=1, column=1)

root.mainloop()
