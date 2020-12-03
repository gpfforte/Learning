from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import filedialog
import sqlite3

root = Tk()
root.title("Learning Python")
root.iconbitmap("Images/Icona.ico")
root.geometry("400x600")


class Table:
    # Crea una tabella passando una finestra ed una lista
    def __init__(self, window, lista):
        total_rows = len(lista)
        total_columns = len(lista[0])
        # code for creating table
        for i in range(total_rows):
            for j in range(total_columns):
                self.e = Entry(window, width=15, fg='black',
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
                list = tabella.grid_slaves()
                for l in list:
                    l.destroy()
            else:
                tabella = Tk()
                tabella.title("Tabella")
                tabella.iconbitmap("Images/Icona.ico")
                tabella.geometry("1000x400")

            intestazioni=["First Name","Last Name","Address","City","State","Zipcode","Id Cliente"]
            for i in range (len(intestazioni)):
                e=Label(tabella, text=intestazioni[i])
                e.grid(row=0, column=i)

            # f_name_label = Label(tabella, text="First Name")
            # f_name_label.grid(row=0, column=0)
            #
            # l_name_label = Label(tabella, text="Last Name")
            # l_name_label.grid(row=0, column=1)
            #
            # address_label = Label(tabella, text="Address")
            # address_label.grid(row=0, column=2)
            #
            # city_label = Label(tabella, text="City")
            # city_label.grid(row=0, column=3)
            #
            # state_label = Label(tabella, text="State")
            # state_label.grid(row=0, column=4)
            #
            # zipcode_label = Label(tabella, text="Zipcode")
            # zipcode_label.grid(row=0, column=5)
            #
            # id_cliente_label = Label(tabella, text="Id Cliente")
            # id_cliente_label.grid(row=0, column=6)
            t = Table(tabella, records)
            # print(records)
            # print_records = ''
            i = len(records)+1 # Considero una riga di intestazione
            # print (records)
            # for record in records:
                # i += 1
                # print_records += str(record[0] + " " + str(record[1]) + " " + str(record[6]) +"\n")
                # f_name_label = Label(tabella, text=str(record[0]))
                # f_name_label.grid(row=i, column=0)
                #
                # l_name_label = Label(tabella, text=str(record[1]))
                # l_name_label.grid(row=i, column=1)
                #
                # address_label = Label(tabella, text=str(record[2]))
                # address_label.grid(row=i, column=2)
                #
                # city_label = Label(tabella, text=str(record[3]))
                # city_label.grid(row=i, column=3)
                #
                # state_label = Label(tabella, text=str(record[4]))
                # state_label.grid(row=i, column=4)
                #
                # zipcode_label = Label(tabella, text=str(record[5]))
                # zipcode_label.grid(row=i, column=5)
                #
                # id_cliente_label = Label(tabella, text=str(record[6]))
                # id_cliente_label.grid(row=i, column=6)

            select_box = Entry(tabella, width=30)
            select_box.grid(row=i+1, column=1, columnspan=3)

            select_box_label = Label(tabella, text="Select ID Cliente")
            select_box_label.grid(row=i+1, column=0)
                
            # query_label = Label(tabella, text=print_records)
            # query_label.grid(row=2, column=0, columnspan=2)
            conn.commit()
            conn.close()
            # Create Delete Button
            delete_btn = Button(tabella, text="Delete Record", command=lambda: delete(select_box.get()))
            delete_btn.grid(row=i+2, column=0)

            # Create Update Button
            edit_btn = Button(tabella, text="Edit Record", command=lambda: edit(select_box.get()))
            edit_btn.grid(row=i+2, column=1)

            close_btn = Button(tabella, text="Close Window", command=tabella.destroy)
            close_btn.grid(row=i+2, columns=6)

            aggiorna_btn=Button(tabella,text="Aggiorna", command=lambda: query("Da Tabella"))
            aggiorna_btn.grid(row=i+3,column=0)


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

id_cliente = Entry(root, width=30)
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
