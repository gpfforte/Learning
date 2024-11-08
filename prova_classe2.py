import email
import os
import sqlite3
import traceback
from tkinter import BOTH, END, LEFT, TOP, Tk, W, messagebox, ttk
from turtle import bgcolor

import pandas as pd
from matplotlib.pyplot import text
from PIL import Image, ImageTk

from servizio.classi import MyTab

# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


class MyApp:
    def __init__(self):
        # # Initialize style
        # s = ttk.Style()
        # # Create style used by default for all Frames
        # s.configure('TFrame', background='green')
        self.root = Tk()
        self.root.geometry("1200x800+50+50")
        self.top_frame = ttk.Frame(self.root, border=1, borderwidth=5)
        # self.top_frame.pack(fill=BOTH, expand=True, anchor="n")
        self.top_frame.pack(anchor="nw")
        self.btn_chiudi = ttk.Button(self.top_frame, text="Chiudi", command=self.chiudi)
        self.btn_chiudi.pack(side=LEFT, anchor="n")
        self.my_notebook = ttk.Notebook(self.root)
        self.my_notebook.pack(fill=BOTH, expand=1, pady=5, padx=5, anchor="n")
        self.tab_prova = MyTab(
            self.my_notebook, "Prova", ("Prova", "Riprova"), table=False
        )
        self.tab_prova.my_listbox.destroy()

        self.first_label = ttk.Label(self.tab_prova.frame_data, text="First Name")
        self.first_label.grid(row=0, column=0, padx=5, pady=5)
        self.first_entry = ttk.Entry(self.tab_prova.frame_data)
        self.first_entry.grid(row=0, column=1, padx=5, pady=5)

        self.last_label = ttk.Label(self.tab_prova.frame_data, text="Last Name")
        self.last_label.grid(row=0, column=2, padx=5, pady=5)
        self.last_entry = ttk.Entry(self.tab_prova.frame_data)
        self.last_entry.grid(row=0, column=3, padx=5, pady=5)

        self.email_label = ttk.Label(self.tab_prova.frame_data, text="Email")
        self.email_label.grid(row=1, column=0, padx=5, pady=5)
        self.email_entry = ttk.Entry(self.tab_prova.frame_data)
        self.email_entry.grid(row=1, column=1, padx=5, pady=5)

        self.phone_label = ttk.Label(self.tab_prova.frame_data, text="Phone")
        self.phone_label.grid(row=1, column=2, padx=5, pady=5)
        self.phone_entry = ttk.Entry(self.tab_prova.frame_data)
        self.phone_entry.grid(row=1, column=3, padx=5, pady=5)

        self.btn_insert = ttk.Button(
            self.tab_prova.frame_top, text="Insert DB", command=lambda: self.insert_db()
        )
        self.btn_insert.pack(side="left", pady=5, padx=5)
        self.btn_select = ttk.Button(
            self.tab_prova.frame_top,
            text="Select from DB",
            command=lambda: self.select_db(),
        )
        self.btn_select.pack(side="left", pady=5, padx=5)
        self.tree = None
        # self.btn_print = ttk.Button(
        #     self.tab_prova.frame_top, text="Print Selected Item", command=lambda: self.print_lb())
        # self.btn_print.pack(side="left", pady=5, padx=5)
        self.conn = sqlite3.connect("my_db.sqlite")
        self.cur = self.conn.cursor()
        # self.cur.execute("""CREATE TABLE IF NOT EXISTS contacts (
        #                                 contact_id INTEGER PRIMARY KEY,
        #                                 first_name TEXT NOT NULL,
        #                                 last_name TEXT NOT NULL,
        #                                 email TEXT NOT NULL UNIQUE,
        #                                 phone TEXT NOT NULL UNIQUE
        #                                 );""")

        self.conn.commit()

        self.root.mainloop()

    def insert_db(self):
        first_name = self.first_entry.get()
        last_name = self.last_entry.get()
        mail = self.email_entry.get()
        phone = self.phone_entry.get()

        sql_string = f"""INSERT INTO contacts (first_name, last_name, email, phone) 
                                    values ('{first_name}', '{last_name}','{mail}', '{phone}')"""
        print(sql_string)
        self.cur.execute(sql_string)
        self.conn.commit()
        self.select_db()

    def select_db(self):
        sql_string = (
            """select contact_id, first_name, last_name, email, phone from contacts"""
        )
        print(sql_string)
        self.cur.execute(sql_string)
        self.records = self.cur.fetchall()
        # for record in self.records:
        #     self.tab_prova.my_listbox.insert("end", record)
        cols = [description[0] for description in self.cur.description]
        self.tab_prova.df = pd.DataFrame(self.records, columns=cols)

        # self.tab_prova.pt.model.df = df
        # self.tab_prova.pt.redraw()
        if not self.tree:
            self.tree = ttk.Treeview(self.tab_prova.frame_table, show="headings")
            self.tree.grid(pady=5, padx=5)
        if self.tree:
            self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = cols
        for i in cols:
            self.tree.column(i, anchor="w")
            self.tree.heading(i, text=i, anchor="w")
        print(self.tab_prova.df)

        for index, row in self.tab_prova.df.iterrows():
            # print(row)
            print(list(row))
            self.tree.insert("", END, values=list(row))

    # def print_lb(self):
    #     for i in self.tab_prova.my_listbox.curselection():
    #         print(self.tab_prova.my_listbox.get(i))

    def chiudi(self):
        self.conn.close()
        self.root.destroy()


def main():
    app = MyApp()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()

