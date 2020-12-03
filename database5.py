from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox, Entry
from tkinter import filedialog
import sqlite3
import csv
import locale
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *

root = Tk()
root.title("Learning Python")
root.iconbitmap("Images/Icona.ico")
root.geometry("400x600")


def aggiorna_tree(tree, records):
    tree.delete(*tree.get_children())
    for i in records:
        tree.insert("","end", values=i)

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
            id_cliente.configure(state="enabled")
            id_cliente.delete(0, END)
            id_cliente.configure(state="disabled")


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

def clear():
    f_name.delete(0, END)
    l_name.delete(0, END)
    address.delete(0, END)
    city.delete(0, END)
    state.delete(0, END)
    zipcode.delete(0, END)
    id_cliente.configure(state="enabled")
    id_cliente.delete(0, END)
    id_cliente.configure(state="disabled")



def crea_tabella_win(cursor):
    global intestazioni
    global f_name
    global l_name
    global address
    global city
    global state
    global zipcode
    global id_cliente

    tabella = Tk()
    tabella.title("Tabella")
    tabella.iconbitmap("Images/Icona.ico")
    tabella.geometry("1000x700")
    tabella.resizable(False,False)

    framedata = Labelframe(tabella,text="Search Result")
    framedata.pack(fill=BOTH,expand=1)
    mediumframe = Labelframe(tabella,text="Record")
    mediumframe.configure(relief=GROOVE, borderwidth=1,width=1000, height=40)
    # bottomframe.grid(row=1,column=0, sticky="sew")
    mediumframe.pack(fill=BOTH, expand=1)
    intestazioni = [description[0] for description in cursor.description]
    # ["First Name", "Last Name", "Address", "City", "State", "Zipcode", "Id Cliente"]
    tree=Treeview(framedata, columns=intestazioni, show="headings", height="9")
    tree.pack(side=LEFT)
    tree.place(x=0,y=0)
    
    for i in range(len(intestazioni)):
        tree.heading(i,text=intestazioni[i])
        tree.column(i,width=150, minwidth=200)
    
    ysb = ttk.Scrollbar(framedata, orient=VERTICAL, command=tree.yview)
    ysb.pack(side=RIGHT,fill="y")
    tree.configure(yscrollcommand=ysb.set)

    xsb = ttk.Scrollbar(framedata, orient=HORIZONTAL, command=tree.xview)
    xsb.pack(side=BOTTOM,fill="x")
    tree.configure(xscrollcommand=xsb.set)
    
    # Entry
    f_name_label = Label(mediumframe, text="First Name")
    f_name_label.grid(row=0, column=0)
    f_name = Entry(mediumframe, width=30)
    f_name.grid(row=0, column=1)

    l_name_label = Label(mediumframe, text="Last Name")
    l_name_label.grid(row=1, column=0)
    l_name = Entry(mediumframe, width=30)
    l_name.grid(row=1, column=1)

    address_label = Label(mediumframe, text="Address")
    address_label.grid(row=2, column=0)
    address = Entry(mediumframe, width=30)
    address.grid(row=2, column=1)

    city_label = Label(mediumframe, text="City")
    city_label.grid(row=0, column=3)
    city = Entry(mediumframe, width=30)
    city.grid(row=0, column=4)

    state_label = Label(mediumframe, text="State")
    state_label.grid(row=1, column=3)
    state = Entry(mediumframe, width=30)
    state.grid(row=1, column=4)

    zipcode_label = Label(mediumframe, text="Zipcode")
    zipcode_label.grid(row=2, column=3)
    zipcode = Entry(mediumframe, width=30)
    zipcode.grid(row=2, column=4)

    id_cliente_label = Label(mediumframe, text="Id Cliente")
    id_cliente_label.grid(row=3, column=0)
    id_cliente = Entry(mediumframe, width=30)
    id_cliente.grid(row=3, column=1)
    


    bottomframe = Labelframe(tabella,text="Opzioni")
    bottomframe.configure(relief=GROOVE, borderwidth=1,width=1000, height=40)
    # bottomframe.grid(row=1,column=0, sticky="sew")
    bottomframe.pack(fill=BOTH, expand=1)
    # Create Delete Button
    delete_btn = Button(bottomframe, text="Delete Record", command=lambda: delete(id_selezionato))
    delete_btn.grid(row=0, column=0,padx=10, pady=10)

    # Create Update Button
    edit_btn = Button(bottomframe, text="Edit Record", command=lambda: edit(id_selezionato))
    edit_btn.grid(row=0, column=1,padx=10, pady=10)

    aggiorna_btn=Button(bottomframe,text="Aggiorna", command=lambda: gestione_clienti("Da Tabella"))
    aggiorna_btn.grid(row=0,column=2,padx=10, pady=10)

    add_btn = Button(bottomframe, text="Add record to database", command=add)
    add_btn.grid(row=0, column=3, pady=10, padx=10)

    clear_btn=Button(bottomframe,text="Clear", command=clear)
    clear_btn.grid(row=0,column=4,padx=10, pady=10)

    csv_btn=Button(bottomframe,text="Export", command=lambda: write_to_csv(records))
    csv_btn.grid(row=0,column=5,padx=10, pady=10)
    


    return tree

 

def gestione_clienti(provenienza):
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
                global tree
                aggiorna_tree(tree, records)
            else:
                tree=crea_tabella_win(cursor)
                aggiorna_tree(tree,records)

                def popola():
                    f_name.delete(0, END)
                    l_name.delete(0, END)
                    address.delete(0, END)
                    city.delete(0, END)
                    state.delete(0, END)
                    zipcode.delete(0, END)
                    id_cliente.configure(state="enabled")
                    id_cliente.delete(0, END)
                    id_cliente.configure(state="disabled")
                    # Create cursor
                    # Create or connect a database
                    conn = sqlite3.connect('address_book.db')

                    # Create cursor                 
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM addresses WHERE oid=" + id_selezionato)
                    records = cursor.fetchall()  # one --- many ---
                    conn.commit()
                    conn.close()
                    if records.__len__() == 1:
                        id_cliente.configure(state="enabled")
                        for record in records:
                            f_name.insert(0, record[0])
                            l_name.insert(0, record[1])
                            address.insert(0, record[2])
                            city.insert(0, record[3])
                            state.insert(0, record[4])
                            zipcode.insert(0, record[5])
                            id_cliente.insert(0, record[6])
                        id_cliente.configure(state="disabled")

                def getrow_and_popola(event):
                    global id_selezionato
                    row_id = tree.identify_row(event.y)
                    item = tree.item(tree.focus())
                    # print(item)
                    # print (intestazioni.index("id_cliente"))
                    id_selezionato=str(item["values"][(intestazioni.index("id_cliente"))])
                    popola()

                tree.bind("<Double 1>", getrow_and_popola)
                
                # tree.bind("<Button 1>", getrow)




        else:
            messagebox.showinfo("Warning", "Non ci sono dati da mostrare")
        conn.commit()
        conn.close()
    except Exception as ex:
        messagebox.showinfo("Errore nel mostrare dati", ex)




# Create Query Button
query_btn = Button(root, text="Gestione Clienti", command=lambda: gestione_clienti("Da Root"))
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
