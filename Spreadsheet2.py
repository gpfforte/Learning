from tkinter import *
import pandas as pd
from tkinter import ttk, filedialog
from openpyxl.workbook import Workbook

from openpyxl import load_workbook

namefile= "countries_red.xlsx"
root = Tk()
root.title('Learning Python')
root.geometry("1000x700")
root.iconphoto(True, PhotoImage(file='Images/Icona.png'))

def file_open():
    filename=filedialog.askopenfilename(
        initialdir="",
        title="Open a file",
        filetype=(("xlsx files", "*.xlsx"), ("All Files", "*.*"))
    )
    if filename:
        try:
            filename=r"{}".format(filename)
            df=pd.read_excel(filename)
        except ValueError:
            my_label.config(text="Not Open")
        except FileNotFoundError:
            my_label.config(text="Not Found")
        clear_tree()
        my_tree["column"]=list(df.columns)
        my_tree["show"]="headings"
        for column in my_tree["column"]:
            my_tree.heading(column, text=column)
        df_rows=df.to_numpy().tolist()
        for row in df_rows:
            my_tree.insert("", END, values=row)
        my_tree.pack()

def clear_tree():
    my_tree.delete(*my_tree.get_children())



my_frame=Frame(root)
my_frame.pack(pady=20)
my_tree=ttk.Treeview(my_frame)
my_menu=Menu(root)
root.config(menu=my_menu)
file_menu=Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Spreadsheets", menu=file_menu)
file_menu.add_command(label="Open xlsx", command=file_open)

my_label=Label(root, text="")
my_label.pack(pady=20)

root.mainloop()
