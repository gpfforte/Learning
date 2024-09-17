'''
Here the TreeView widget is configured as a multi-column listbox
with adjustable column width and column-header-click sorting.
'''

import tkinter as tk
import pandas as pd
from servizio.classi import MyTreeview, MyTab
from tkinter import ttk
import os

# the test data ...
# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


car_header = ['car', 'repair', 'test', 'ora', 'et labora']
car_list = [
    ('Hyundai', 'brakes', '1', 'brakes', '1'),
    ('Honda', 'light', '2', 'brakes', '1'),
    ('Lexus', 'battery', '3', 'brakes', '1'),
    ('Benz', 'wiper', '4', 'brakes', '1'),
    ('Ford', 'tire', '5', 'brakes', '1'),
    ('Chevy', 'air', '6', 'brakes', '1'),
    ('Chrysler', 'piston', '7', 'brakes', '1'),
    ('Toyota', 'brake pedal', '8', 'brakes', '1'),
    ('BMW', 'seat', '9', 'brakes', '1'),
    ('Hyundai', 'brakes', '1', 'brakes', '1'),
    ('Honda', 'light', '2', 'brakes', '1'),
    ('Lexus', 'battery', '3', 'brakes', '1'),
    ('Benz', 'wiper', '4', 'brakes', '1'),
    ('Ford', 'tire', '5', 'brakes', '1'),
    ('Chevy', 'air', '6', 'brakes', '1'),
    ('Chrysler', 'piston', '7', 'brakes', '1'),
    ('Toyota', 'brake pedal', '8', 'brakes', '1'),
    ('BMW', 'seat', '9', 'brakes', '1'),
]
df_cars = pd.DataFrame(car_list, columns=car_header)
# print(df_cars)

df_sample = pd.read_csv("sample.csv", sep=";")

df_empty = pd.DataFrame()

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Multicolumn Treeview/Listbox")
    root.geometry('1000x700+200+100')
    style = ttk.Style()
    style.theme_use("clam")
    style.configure('Emergency.TButton', font='helvetica 24', foreground='red',
                    background='yellow', padding=10)

    my_notebook = ttk.Notebook(root)
    my_notebook.pack(fill=tk.BOTH, expand=1, pady=5, padx=5)
    radio_tupla = ("Totali", "Per gruppo...")
    tab_prova = MyTab(my_notebook, "Prova", radio_tupla, False)

    listbox_treeview = tab_prova.my_treeview

    # def empty_tree():
    #     listbox.update_data(df_empty)

    def fill_tree():
        listbox_treeview.update_data(df_sample)

    # def selected_item():
    #     print(listbox.tree.item(listbox.tree.focus(), "values"))
    #     print(listbox.tree.focus())

    my_frame2 = ttk.Frame(root).pack(padx=10, pady=10)

    # ttk.Button(my_frame2, text='Selected', command=selected_item).pack(
    #     fill='both')
    # ttk.Button(my_frame2, text='Empty Tree', command=empty_tree).pack(
    #     fill='both')
    ttk.Button(my_frame2, text='Fill Tree', command=fill_tree).pack(
        fill='both')
    ttk.Button(my_frame2, text='Close', command=root.destroy,
               style='Emergency.TButton').pack(fill='both')
    # ttk.Button(my_frame2, text='Selected', command=selected_item).grid(
    #     row=0, column=0, sticky='we')
    # ttk.Button(my_frame2, text='Close', command=root.destroy, style='Emergency.TButton').grid(
    #     row=0, column=0, sticky='we')
    root.mainloop()
