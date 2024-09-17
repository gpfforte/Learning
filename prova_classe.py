import email
import os
import sqlite3
from tkinter import BOTH, LEFT, TOP, Listbox, Tk, messagebox, ttk
from turtle import bgcolor

from PIL import Image, ImageTk

from servizio.classi import MyTab


class MyApp:
    def __init__(self):
        # # Initialize style
        # s = ttk.Style()
        # # Create style used by default for all Frames
        # s.configure('TFrame', background='green')
        self.root = Tk()
        self.root.geometry("800x600+50+50")
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
        self.btn_insert = ttk.Button(
            self.tab_prova.frame_top,
            text="Insert DB",
            command=lambda: self.insert_db(self.tupla),
        )
        self.btn_insert.pack(side="left", pady=5, padx=5)
        self.btn_select = ttk.Button(
            self.tab_prova.frame_top,
            text="Select from DB",
            command=lambda: self.select_db(),
        )
        self.btn_select.pack(side="left", pady=5, padx=5)
        self.btn_print = ttk.Button(
            self.tab_prova.frame_top,
            text="Print Selected Item",
            command=lambda: self.print_lb(),
        )
        self.btn_print.pack(side="left", pady=5, padx=5)
        self.my_listbox = Listbox(self.tab_prova.frame_data)
        self.my_listbox.pack(side="left", pady=5, padx=5)
        self.conn = sqlite3.connect("my_db.sqlite")
        self.cur = self.conn.cursor()
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS contacts (
                                        contact_id INTEGER PRIMARY KEY,
                                        first_name TEXT NOT NULL,
                                        last_name TEXT NOT NULL,
                                        email TEXT NOT NULL UNIQUE,
                                        phone TEXT NOT NULL UNIQUE
                                        );"""
        )
        self.tupla = contact_id1, first_name1, last_name1, email1, phone = (
            3,
            "Era",
            "Su",
            "choy@trui.com",
            "0284710000",
        )

        self.conn.commit()

        self.root.mainloop()

    def insert_db(self, tupla):
        contact_id, first_name, last_name, mail, phone = tupla
        sql_string = f"""INSERT INTO contacts values ('{contact_id}', '{first_name}', 
                    '{last_name}','{mail}', '{phone}')"""
        print(sql_string)
        self.cur.execute(sql_string)
        self.conn.commit()

    def select_db(self):
        sql_string = (
            """select contact_id, first_name, last_name, email, phone from contacts"""
        )
        print(sql_string)
        self.cur.execute(sql_string)
        self.records = self.cur.fetchall()
        for record in self.records:
            self.my_listbox.insert("end", record)

    def print_lb(self):
        for i in self.tab_prova.my_listbox.curselection():
            print(self.tab_prova.my_listbox.get(i))

    def chiudi(self):
        self.conn.close()
        self.root.destroy()


if __name__ == "__main__":
    app = MyApp()

