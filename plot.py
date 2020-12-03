from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import filedialog
import requests
import json
import numpy as np
import matplotlib.pyplot as plt

root=Tk()
root.title("Learning Python")
root.iconbitmap("Images/Icona.ico")
root.geometry("400x200")

def graph():
    house_prices=np.random.normal(200000,25000,5000)
    plt.hist(house_prices,500)
    plt.show()

my_btn= Button(root,text="Graph", command= graph)
my_btn.pack()

root.mainloop()
