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
import os

global dati_mostrati


root = Tk()
root.title("Learning Python")
# root.iconphoto(True, PhotoImage(file='Images/Icona.png'))
# root.iconbitmap("Images/Icona.bmp")
root.geometry("400x600")

def aggiorna_tree_search(tree,*search):
    # Questa funzione riceve in input il tree da aggiornare o un ulteriore parametro per fare una ricerca con il like
    global dati_mostrati
    tree.delete(*tree.get_children())
    try:
        # Create or connect a database
        conn = sqlite3.connect('address_book.db')
        # print(search)
        # Create cursor
        cursor = conn.cursor()
        if not search or search[0]=="":
            cursor.execute("SELECT * FROM addresses")
        else:
            search = search[0]
            cursor.execute("""SELECT * FROM addresses where
             first_name like ?
             or last_name like ? 
             or city like ? 
             or address like ?
             or state like ?
             or zipcode like ?
             or id_cliente like ?""",
            ('%'+search+'%', '%'+search+'%', '%'+search+'%', '%'+search+'%', '%'+search+'%', '%'+search+'%', '%'+search+'%'))
        records = cursor.fetchall()  # one --- many ---
        for i in records:
            tree.insert("", "end", values=i)
        conn.commit()
        conn.close()
        dati_mostrati=records
        return records
    except Exception as ex:
        messagebox.showinfo("Errore aggiornamento Tree", ex, parent=tabella)


def save(record_id,tree):
    try:
        if record_id > "":
            conn = sqlite3.connect('address_book.db')
            cursor = conn.cursor()
            riga=[f_name.get(),l_name.get(),address.get(),city.get(),state.get(),zipcode.get(),record_id]
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
            aggiorna_tree_search(tree)
            # editor.destroy()
        else:
            messagebox.showinfo("Errore salvataggio", "l'Id deve essere popolato", parent=tabella)
    except Exception as ex:
        messagebox.showinfo("Errore nel save", ex, parent=tabella)
    # query("Da Aggiornamento")



def delete(record_id,tree):
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
                response=messagebox.askquestion("Cancellazione Cliente", "Sei sicuro di cancellare il cliente "+record_id+" ?",parent=tabella)
                # print(response)
                if response=="yes":

                    if records.__len__() == 1:
                        cursor.execute("DELETE FROM addresses WHERE id_cliente=" + record_id
                                       )
                    else:
                        messagebox.showinfo("Errore update", "Non esiste alcun record con id = " + record_id, parent=tabella)

                conn.commit()
                conn.close()

        except Exception as ex:
            messagebox.showinfo("Errore nella cancellazione", ex, parent=tabella)
    else:
        messagebox.showinfo("Errore cancellazione", "l'Id deve essere popolato",parent=tabella)
    aggiorna_tree_search(tree)
    clear()

def add(tree):
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
            aggiorna_tree_search(tree)
        except Exception as ex:
            messagebox.showinfo("Errore nell'inserimento", ex, parent=tabella)
    else:
        messagebox.showinfo("Errore nell'inserimento", "Il First name deve essere popolato", parent=tabella)
    
def write_to_csv(dati_mostrati):
    with open("customers.csv","a", newline="") as f:
        w=csv.writer(f, dialect="excel")
        for record in dati_mostrati:
            w.writerow(record)

def clear():
    global id_selezionato
    f_name.delete(0, END)
    l_name.delete(0, END)
    address.delete(0, END)
    city.delete(0, END)
    state.delete(0, END)
    zipcode.delete(0, END)
    id_cliente.configure(state="enabled")
    id_cliente.delete(0, END)
    id_cliente.configure(state="disabled")
    id_selezionato=""



def crea_tabella_win(cursor):
    global tabella
    global id_selezionato
    global intestazioni
    global f_name
    global l_name
    global address
    global city
    global state
    global zipcode
    global id_cliente
    global dati_mostrati
    dati_mostrati=""
    id_selezionato = ""
    # tabella = Tk()
    tabella=Toplevel(root)
    tabella.title("Tabella")
    # tabella.iconbitmap("Images/Icona.ico")
    tabella.geometry("1000x700")
    tabella.resizable(False,False)

    topframe = Labelframe(tabella,text="Search...")
    topframe.pack(fill=BOTH)

    search_btn = Button(topframe, text="Cerca", command=lambda: aggiorna_tree_search(tree, search_label_entry.get()))
    search_btn.grid(row=1, column=0, pady=10, padx=10)
    
    search_label_entry = Entry(topframe, width=30)
    search_label_entry.grid(row=1, column=1)
    search_label_entry.bind("<Return>", lambda event: aggiorna_tree_search(tree, search_label_entry.get()))

    mediumframe = Labelframe(tabella,text="Record")
    # mediumframe.configure(relief=GROOVE, borderwidth=1,width=1000, height=40)
    mediumframe.configure(relief=GROOVE, borderwidth=1)#,width=1000, height=40)
    # bottomframe.grid(row=1,column=0, sticky="sew")
    mediumframe.pack(fill=BOTH)
    bottomframe = Labelframe(tabella,text="Opzioni")
    bottomframe.configure(relief=GROOVE, borderwidth=1,width=1000, height=40)
    # bottomframe.grid(row=1,column=0, sticky="sew")
    bottomframe.pack(fill=BOTH)

    framedata = Labelframe(tabella,text="Search Result")
    framedata.pack(fill=BOTH,expand=1)

    intestazioni = [description[0] for description in cursor.description]
    # ["First Name", "Last Name", "Address", "City", "State", "Zipcode", "Id Cliente"]
    tree=Treeview(framedata, columns=intestazioni, show="headings", height="18")
    tree.pack(side=LEFT)
    tree.place(x=0,y=0)
    style = ttk.Style()
    # style.configure(".", font=('Helvetica', 8), foreground="white")
    style.configure("Treeview.Heading", foreground='black')
    style.configure("Treeview.Heading", font=('Calibri',15 ,'bold'))
    
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
    f_name_label.grid(row=0, column=0,padx=10, pady=5)
    f_name = Entry(mediumframe, width=30)
    f_name.grid(row=0, column=1,padx=10, pady=5)

    l_name_label = Label(mediumframe, text="Last Name")
    l_name_label.grid(row=1, column=0,padx=10, pady=5)
    l_name = Entry(mediumframe, width=30)
    l_name.grid(row=1, column=1,padx=10, pady=5)

    address_label = Label(mediumframe, text="Address")
    address_label.grid(row=2, column=0,padx=10, pady=5)
    address = Entry(mediumframe, width=30)
    address.grid(row=2, column=1,padx=10, pady=5)

    city_label = Label(mediumframe, text="City")
    city_label.grid(row=0, column=3,padx=10, pady=5)
    city = Entry(mediumframe, width=30)
    city.grid(row=0, column=4,padx=10, pady=5)

    state_label = Label(mediumframe, text="State")
    state_label.grid(row=1, column=3,padx=10, pady=5)
    state = Entry(mediumframe, width=30)
    state.grid(row=1, column=4,padx=10, pady=5)

    zipcode_label = Label(mediumframe, text="Zipcode")
    zipcode_label.grid(row=2, column=3,padx=10, pady=5)
    zipcode = Entry(mediumframe, width=30)
    zipcode.grid(row=2, column=4,padx=10, pady=5)

    id_cliente_label = Label(mediumframe, text="Id Cliente")
    id_cliente_label.grid(row=3, column=0,padx=10, pady=5)
    id_cliente = Entry(mediumframe, width=30)
    id_cliente.grid(row=3, column=1,padx=10, pady=5)

    # Create Delete Button
    delete_btn = Button(bottomframe, text="Delete Record", command=lambda: delete(id_selezionato,tree))
    delete_btn.grid(row=0, column=0,padx=10, pady=10)

    # Create Save Button
    save_btn = Button(bottomframe, text="Save Record", command=lambda: save(id_selezionato,tree))
    save_btn.grid(row=0, column=1,padx=10, pady=10)

    refresh_btn=Button(bottomframe,text="Refresh Tree", command=lambda: gestione_clienti("Da Tabella"))
    refresh_btn.grid(row=0,column=2,padx=10, pady=10)

    add_btn = Button(bottomframe, text="Add record to database", command=lambda: add(tree))
    add_btn.grid(row=0, column=3, pady=10, padx=10)

    clear_btn=Button(bottomframe,text="Clear", command=clear)
    clear_btn.grid(row=0,column=4,padx=10, pady=10)

    csv_btn=Button(bottomframe,text="Export", command=lambda: write_to_csv(dati_mostrati))
    csv_btn.grid(row=0,column=5,padx=10, pady=10)



    return tree


def popola(id_selezionato):
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
    id_selezionato = str(item["values"][(intestazioni.index("id_cliente"))])
    popola(id_selezionato)
 

def gestione_clienti(provenienza):
    try:
        if provenienza!="Da Root":
            global tree
            records=aggiorna_tree_search(tree)
        else:
            conn = sqlite3.connect('address_book.db')

            # Create cursor
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM addresses")
            records = cursor.fetchall()  # one --- many ---
            tree=crea_tabella_win(cursor)
            conn.commit()
            conn.close()
            records=aggiorna_tree_search(tree)



            tree.bind("<Double 1>", getrow_and_popola)

            # tree.bind("<Button 1>", getrow)




        # else:
        #     messagebox.showinfo("Warning", "Non ci sono dati da mostrare")
        # conn.commit()
        # conn.close()
    except Exception as ex:
        messagebox.showinfo("Errore nel mostrare dati", ex, parent=tabella)




# Create Query Button
clienti_btn = Button(root, text="Gestione Clienti", command=lambda: gestione_clienti("Da Root"))
clienti_btn.grid(row=8, column=0, columnspan=2, pady=10, padx=10, ipadx=137)



root.mainloop()
