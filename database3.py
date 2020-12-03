from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox, Entry
from tkinter import filedialog
import sqlite3
import csv
import locale
import pandas as pd
from pandastable import Table


root = Tk()
root.title("Learning Python")
root.iconbitmap("Images/Icona.ico")
root.geometry("400x600")



class Tabella_entry:
    # Crea una tabella passando un oggetto ed una lista
    def __init__(self, widget, lista):
        total_rows = len(lista)
        total_columns = len(lista[0])
        # code for creating table
        for i in range(total_rows):
            for j in range(total_columns):
                self.e = Entry(widget, width=15, fg='black',
                               font=('Arial', 10, 'normal'))

                self.e.grid(row=i+1, column=j)
                self.e.insert(END, lista[i][j])

 # Create or connect a database
# conn=sqlite3.connect('address_book.db')

# Create cursor
# cursor=conn.cursor()
'''
cursor.execute(""" CREATE TABLE addresses(
                first_name text,
                last_name text,
                address text,
                city text,
                state text,
                zipcode integer
                )""")
"""
'''


def save(record_id):
    try:

        conn = sqlite3.connect('address_book.db')
        cursor = conn.cursor()
        riga=[f_name_editor.get(),l_name_editor.get(),address_editor.get(),city_editor.get(),state_editor.get(),zipcode_editor.get(),record_id]
        #cursor.execute("INSERT INTO addresses VALUES (?,?,?,?,?,?,NULL)", riga)
        cursor.execute("""UPDATE addresses SET 
            first_name=?,
            last_name=?,
            address=?,
            city=?,
            state=?,
            zipcode=?
            WHERE id_cliente =?""",riga
                        )

        conn.commit()
        conn.close()
        editor.destroy()
    except Exception as ex:
        messagebox.showinfo("Errore nel save", ex)
    query("Da Aggiornamento")

def edit(record_id):
    # Capisco se è stato selezionato un numero intero, altrimenti la query va in errore
    integer = 1
    try:
        int(record_id)
    except Exception:
        integer = 0
    try:
        if record_id > "" and integer:

            conn = sqlite3.connect('address_book.db')

            # Create cursor
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM addresses WHERE oid=" + record_id)
            records = cursor.fetchall()  # one --- many ---
            if records.__len__() == 1:
                global editor
                editor = Tk()
                editor.title("Update a Record")
                editor.iconbitmap("Images/Icona.ico")
                editor.geometry("400x600")

                # Loop thru results

                global f_name_editor
                global l_name_editor
                global address_editor
                global city_editor
                global state_editor
                global zipcode_editor

                # Entry
                f_name_editor = Entry(editor, width=30)
                f_name_editor.grid(row=0, column=1, padx=20, pady=(10, 0))

                l_name_editor = Entry(editor, width=30)
                l_name_editor.grid(row=1, column=1)

                address_editor = Entry(editor, width=30)
                address_editor.grid(row=2, column=1)

                city_editor = Entry(editor, width=30)
                city_editor.grid(row=3, column=1)

                state_editor = Entry(editor, width=30)
                state_editor.grid(row=4, column=1)

                zipcode_editor = Entry(editor, width=30)
                zipcode_editor.grid(row=5, column=1)
                
                id_cliente_editor = Entry(editor, width=30)
                id_cliente_editor.grid(row=6, column=1)
                # id_cliente_editor.configure(state="disabled")
                # Label

                f_name_label_editor = Label(editor, text="First Name")
                f_name_label_editor.grid(row=0, column=0, pady=(10, 0))

                l_name_label_editor = Label(editor, text="Last Name")
                l_name_label_editor.grid(row=1, column=0)

                address_label_editor = Label(editor, text="Address")
                address_label_editor.grid(row=2, column=0)

                city_label_editor = Label(editor, text="City")
                city_label_editor.grid(row=3, column=0)

                state_label_editor = Label(editor, text="State")
                state_label_editor.grid(row=4, column=0)

                zipcode_label_editor = Label(editor, text="Zipcode")
                zipcode_label_editor.grid(row=5, column=0)
                
                id_cliente_label_editor = Label(editor, text="Client Id")
                id_cliente_label_editor.grid(row=6, column=0)

                for record in records:
                    f_name_editor.insert(0, record[0])
                    l_name_editor.insert(0, record[1])
                    address_editor.insert(0, record[2])
                    city_editor.insert(0, record[3])
                    state_editor.insert(0, record[4])
                    zipcode_editor.insert(0, record[5])
                    id_cliente_editor.insert(0, record[6])
                id_cliente_editor.configure(state="disabled")
                # Create Save Button
                save_btn = Button(editor, text="Save Record", command=lambda: save(record_id))
                save_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=137)
            else:
                messagebox.showinfo("Errore update", "Non esiste alcun record con id = "+record_id)
        else:
            messagebox.showinfo("Errore update", "Seleziona un record id valido")
    except Exception as ex:
        messagebox.showinfo("Errore nell'update", ex)


def delete(record_id):
    # record_id = select_box.get()
    if record_id > "":
        
        integer = 1
        try:
            int(record_id)
        except Exception:
            integer = 0
        try:
            if record_id > "" and integer:
                conn = sqlite3.connect('address_book.db')
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM addresses WHERE id_cliente=" + record_id)
                records = cursor.fetchall()  # one --- many ---
                if records.__len__() == 1:
                    cursor.execute("DELETE FROM addresses WHERE id_cliente=" + record_id
                                   )
                else:
                    messagebox.showinfo("Errore update", "Non esiste alcun record con id = " + record_id)

                conn.commit()
                conn.close()

        except Exception as ex:
            messagebox.showinfo("Errore nella cancellazione", ex)
    else:
        messagebox.showinfo("Errore cancellazione", "l'Id deve essere popolato")
    query("Da Delete")

def add():
    if f_name.get() > "":
        try:
            # Create or connect a database
            conn = sqlite3.connect('address_book.db')
            # Create cursor
            cursor = conn.cursor()
            riga = [f_name.get(), l_name.get(), l_name.get(), city.get(), state.get(), zipcode.get()]
            # riga=["ciao","ciao","ciao","ciao","ciao",1]
            # print(riga)

            cursor.execute("INSERT INTO addresses VALUES (?,?,?,?,?,?,NULL)", riga)

            # cursor.execute("INSERT INTO addresses VALUES (:f_name,:l_name,:address,:city,:state,:zipcode)",
            #                {
            #                    'f_name': f_name.get(),
            #                    'l_name': l_name.get(),
            #                    'address': l_name.get(),
            #                    'city': city.get(),
            #                    'state': state.get(),
            #                    'zipcode': zipcode.get()
            #                })
            f_name.delete(0, END)
            l_name.delete(0, END)
            address.delete(0, END)
            city.delete(0, END)
            state.delete(0, END)
            zipcode.delete(0, END)
            id_cliente.delete(0, END)

            conn.commit()

            conn.close()

        except Exception as ex:
            messagebox.showinfo("Errore nell'inserimento", ex)
    else:
        messagebox.showinfo("Errore nell'inserimento", "Il last name deve essere popolato")
    
def write_to_csv(records):
    with open("customers.csv","a", newline="") as f:
        w=csv.writer(f, dialect="excel")
        for record in records:
            w.writerow(record)

def query(provenienza):
    try:
        # Create or connect a database
        conn = sqlite3.connect('address_book.db')

        # Create cursor
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM addresses")
        records = cursor.fetchall()  # one --- many ---
        if records.__len__() > 0:
            global tabella

            if provenienza!="Da Root":
                # list = tabella.grid_slaves()
                list = tabella.pack_slaves()
                for l in list:
                    print(l)
                    l.destroy()
            else:
                tabella = Tk()
                tabella.title("Tabella")
                tabella.iconbitmap("Images/Icona.ico")
                tabella.geometry("1000x400")

            df = pd.DataFrame(records)
            framedata = Frame(tabella)
            # framedata.grid(row=0,sticky="ew")
            framedata.pack(fill=BOTH, expand=1)
            framedata.configure(relief=GROOVE, borderwidth=1)
            pt = Table(framedata, dataframe=df)
            intestazioni = ["First Name", "Last Name", "Address", "City", "State", "Zipcode", "Id Cliente"]
            
            pt.show()
            # questo codice serve per selezionare una riga
            def handle_left_click(event):
                """Handle left click"""
                rowclicked_single = pt.get_row_clicked(event)
                #print(rowclicked_single)
                global id_selezionato
                id_selezionato=str(records[rowclicked_single][6])
                pt.setSelectedRow(rowclicked_single)
                pt.redraw()
            pt.rowheader.bind('<Button-1>', handle_left_click)

            pt.bind("<Button-1>", handle_left_click)
            # frame = Frame(tabella)
            # frame.configure(relief=GROOVE, borderwidth=1)
            # frame.grid(row=0,sticky="ew")
            # t = Tabella_entry(frame, records)


            bottomframe = Frame(tabella)
            bottomframe.configure(relief=GROOVE, borderwidth=1,width=1000, height=40)
            # bottomframe.grid(row=1,column=0, sticky="sew")
            bottomframe.pack(fill=BOTH, expand=1)
            # sideframe = Frame(tabella)
            # sideframe.configure(relief=GROOVE, borderwidth=1, width=1000, height=40)
            # sideframe.grid(row=1, column=1,sticky="sew")

            intestazioni=["First Name","Last Name","Address","City","State","Zipcode","Id Cliente"]
            # for i in range (len(intestazioni)):
            #     e=Label(frame, text=intestazioni[i])
            #     e.grid(row=0, column=i)




            # i = len(records)+1 # Considero una riga di intestazione
            # print (records)
            # for record in records:


            # select_box = Entry(frame, width=30)
            # select_box.grid(row=i+1, column=1, columnspan=3)

            # select_box_label = Label(frame, text="Select ID Cliente")
            # select_box_label.grid(row=i+1, column=0)
                
            # query_label = Label(tabella, text=print_records)
            # query_label.grid(row=2, column=0, columnspan=2)
            conn.commit()
            conn.close()
            # Create Delete Button
            delete_btn = Button(bottomframe, text="Delete Record", command=lambda: delete(id_selezionato))
            delete_btn.grid(row=0, column=0,padx=10, pady=10)

            # Create Update Button
            edit_btn = Button(bottomframe, text="Edit Record", command=lambda: edit(id_selezionato))
            edit_btn.grid(row=0, column=1,padx=10, pady=10)

            aggiorna_btn=Button(bottomframe,text="Aggiorna", command=lambda: query("Da Tabella"))
            aggiorna_btn.grid(row=0,column=2,padx=10, pady=10)

            csv_btn=Button(bottomframe,text="Export", command=lambda: write_to_csv(records))
            csv_btn.grid(row=0,column=3,padx=10, pady=10)

            # close_btn = Button(sideframe, text="Close Window", command=tabella.destroy)
            # close_btn.grid(row=0, columns=10,padx=10, pady=10, sticky="e")

        else:
            messagebox.showinfo("Warning", "Non ci sono dati da mostrare")
    except Exception as ex:
        messagebox.showinfo("Errore nell'inserimento", ex)


# Entry
f_name = Entry(root, width=30)
f_name.grid(row=0, column=1, padx=20, pady=(10, 0))

l_name = Entry(root, width=30)
l_name.grid(row=1, column=1)

address = Entry(root, width=30)
address.grid(row=2, column=1)

city = Entry(root, width=30)
city.grid(row=3, column=1)

state = Entry(root, width=30)
state.grid(row=4, column=1)

zipcode = Entry(root, width=30)
zipcode.grid(row=5, column=1)

id_cliente: Entry = Entry(root, width=30)
id_cliente.grid(row=6, column=1)
id_cliente.configure(state="disabled")

# select_box = Entry(root, width=30)
# select_box.grid(row=9, column=1)

# Label

f_name_label = Label(root, text="First Name")
f_name_label.grid(row=0, column=0, pady=(10, 0))

l_name_label = Label(root, text="Last Name")
l_name_label.grid(row=1, column=0)

address_label = Label(root, text="Address")
address_label.grid(row=2, column=0)

city_label = Label(root, text="City")
city_label.grid(row=3, column=0)

state_label = Label(root, text="State")
state_label.grid(row=4, column=0)

zipcode_label = Label(root, text="Zipcode")
zipcode_label.grid(row=5, column=0)

id_cliente_label = Label(root, text="Id Cliente")
id_cliente_label.grid(row=6, column=0)

# select_box_label = Label(root, text="Select ID")
# select_box_label.grid(row=9, column=0)

# Create Submit Button
add_btn = Button(root, text="Add record to database", command=add)
add_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

# Create Query Button
query_btn = Button(root, text="Show Records", command=lambda: query("Da Root"))
query_btn.grid(row=8, column=0, columnspan=2, pady=10, padx=10, ipadx=137)

# Create Delete Button
# delete_btn = Button(root, text="Delete Record", command= lambda: delete(select_box.get()))
# delete_btn.grid(row=11, column=0, columnspan=2, pady=10, padx=10, ipadx=137)

# Create Update Button
# edit_btn = Button(root, text="Edit Record", command= lambda: edit(select_box.get()))
# edit_btn.grid(row=12, column=0, columnspan=2, pady=10, padx=10, ipadx=137)

# conn.commit()

# conn.close()


root.mainloop()
