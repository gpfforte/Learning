import tkinter as tk
import sqlite3
from tkinter import ttk
import pandas as pd

root = tk.Tk()

database = 'coffee.db'

conn = sqlite3.connect(database)
cursor = conn.cursor()
cursor.execute("select * from coffee")
records = cursor.fetchall()

df = pd.DataFrame(records)
cols = [description[0] for description in cursor.description]

tree = ttk.Treeview(root, show="headings")
tree.pack()
tree["columns"] = cols
for i in cols:
    tree.column(i, anchor="w")
    tree.heading(i, text=i, anchor='w')
print(df)

for index, row in df.iterrows():
    print(row)
    print(list(row))
    tree.insert("", 0, values=list(row))
    # tree.insert("",0,text=index,values=list(row))

root.mainloop()
