from sqlalchemy import inspect
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import User, Address, engine
import pandas as pd
from tkinter import *
from tkinter import ttk
from pandastable import Table, TableModel
from datetime import datetime
from tkinter import messagebox, Entry
import os
import traceback

# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
df = pd.DataFrame()


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}

def popola_indirizzi_utente():
    global df_indirizzi
    session = Session(engine)
    stmt = select(Address).join(User).where(
        User.id == riferimento_dettaglio[0])
    lista = []
    for address in session.scalars(stmt):
        lista.append([address.id, address.email_address])
    df_indirizzi = pd.DataFrame(lista, columns=["ID", "EMAIL"])
    pt1.model.df = df_indirizzi
    pt1.redraw()

def salva_indirizzo_nel_db():
    with Session(engine) as session:
        indirizzo = session.get(Address, entry_address_id.get())
        indirizzo.email_address = entry_address.get()
        session.commit()
    popola_indirizzi_utente()


def crea_indirizzo_nel_db():
    with Session(engine) as session:
        # Le due modalità sotto sono equivalenti, ma una usa una sola riga di codice
        # user = session.get(User, riferimento_dettaglio[0])
        # indirizzo = Address(email_address=entry_address.get(), user=user)
        indirizzo = Address(email_address=entry_address.get(), user_id=riferimento_dettaglio[0])
        session.add(indirizzo)
        session.commit()
    popola_indirizzi_utente()

def cancella_indirizzo_dal_db():
    with Session(engine) as session:
        indirizzo = session.get(Address, entry_address_id.get())
        session.commit()
        if indirizzo:
            session.delete(indirizzo)
            session.commit()
        else:
            messagebox.showerror("L'id non è presente nel DB",
                                 "L'id non è presente nel DB", parent=root)
    popola_indirizzi_utente()

def aggiorna_testata_indirizzo():
    global riferimento_indirizzo
    global entry_address_id
    global entry_address

    entry_address_id.delete(0, 'end')
    entry_address_id.insert(0, riferimento_indirizzo[0])
    entry_address.delete(0, 'end')
    entry_address.insert(0, riferimento_indirizzo[1])


def indirizzi_utente():
    global riferimento_dettaglio
    global entry_address_id
    global entry_address
    global pt1
    session = Session(engine)
    user = session.get(User, riferimento_dettaglio[0])
    tabella = Toplevel(root)
    tabella.title("Indirizzi")
    # tabella.iconbitmap("Images/Icona.ico")
    tabella.geometry("1000x700")
    my_top_frame = ttk.Frame(tabella)
    my_top_frame.pack(fill=BOTH, expand=1, pady=5, padx=5)
    my_medium_frame = ttk.Frame(tabella)
    my_medium_frame.pack(fill=BOTH, expand=1, pady=5, padx=5)
    # label_email_lbl = ttk.Label(my_top_frame, text="Utente")
    # label_email_lbl.pack(side="left", pady=5, padx=5)
    # label_email_value = ttk.Label(my_top_frame, text={user})
    # label_email_value.pack(side="left", pady=5, padx=5)
    for key, value in object_as_dict(user).items():
        _label = ttk.Label(my_top_frame, text=key)
        _label.pack(side="left", pady=5, padx=5)
        _entry = ttk.Entry(my_top_frame)
        _entry.pack(side="left", pady=5, padx=5)
        _entry.delete(0, 'end')
        _entry.insert(0, value)
        _entry.config(state="disabled")

    label_address_id = ttk.Label(my_medium_frame, text="Address Id")
    label_address_id.pack(side="left", pady=5, padx=5)
    entry_address_id = ttk.Entry(my_medium_frame, width=20)
    entry_address_id.pack(side="left", pady=5, padx=5)
    label_address = ttk.Label(my_medium_frame, text="Address")
    label_address.pack(side="left", pady=5, padx=5)
    entry_address = ttk.Entry(my_medium_frame, width=20)
    entry_address.pack(side="left", pady=5, padx=5)

    my_btn_save = ttk.Button(my_medium_frame, text="Salva nel DB",
                             command=lambda: salva_indirizzo_nel_db())
    my_btn_save.pack(side="left", pady=5, padx=5)

    my_btn_crea = ttk.Button(my_medium_frame, text="Crea nel DB",
                             command=lambda: crea_indirizzo_nel_db())
    my_btn_crea.pack(side="left", pady=5, padx=5)

    my_btn_cancella = ttk.Button(my_medium_frame, text="Cancella dal DB",
                                 command=lambda: cancella_indirizzo_dal_db())
    my_btn_cancella.pack(side="left", pady=5, padx=5)


    my_frame = ttk.Frame(tabella)
    my_frame.pack(fill=BOTH, expand=1, pady=5, padx=5)
    pt1 = Table(my_frame, showtoolbar=True, showstatusbar=True)

    popola_indirizzi_utente()

    def handle_left_click(event):
        global riferimento_indirizzo
        """Handle left click"""
        rowclicked_single = pt1.get_row_clicked(event)
        colclicked_single = pt1.get_col_clicked(event)
        # riferimento_dettaglio = df["ID"].iloc[[rowclicked_single]].values[0]
        riferimento_indirizzo = df_indirizzi.iloc[[rowclicked_single]].values[0]
        # print("riferimento_indirizzo", riferimento_indirizzo)
        pt1.setSelectedRow(rowclicked_single)
        aggiorna_testata_indirizzo()
    pt1.bind('<ButtonRelease-1>', handle_left_click)
    pt1.show()
    pt1.redraw()
    # pt1.model.df = df_dettaglio
    #


def popola_dati():
    global df
    session = Session(engine)
    stmt = select(User)
    lista = []
    for user in session.scalars(stmt):
        lista.append([user.id, user.name, user.fullname, user.nickname])

    df = pd.DataFrame(lista, columns=["ID", "NAME", "FULLNAME", "NICKNAME"])
    pt.model.df = df
    pt.redraw()

#df = table.model.df


def salva_utente_nel_db():
    global entry_user_id
    global entry_name
    global entry_fullname
    global entry_nickname

    with Session(engine) as session:
        if user := session.get(User, entry_user_id.get()):
            user.name = entry_name.get()
            user.fullname = entry_fullname.get()
            user.nickname = entry_nickname.get()
            session.commit()
        else:
            messagebox.showerror("L'id non è presente nel DB",
                                 "L'id non è presente nel DB", parent=root)
    popola_dati()


def crea_utente_nel_db():
    global entry_user_id
    global entry_name
    global entry_fullname
    global entry_nickname

    with Session(engine) as session:
        user = User(name=entry_name.get(),
                    fullname=entry_fullname.get(), nickname=entry_nickname.get())
        # user.name = entry_name.get()
        # user.fullname = entry_fullname.get()
        # user.nickname = entry_nickname.get()
        session.add(user)
        session.commit()
    popola_dati()


def cancella_utente_dal_db():
    global entry_user_id
    global entry_name
    global entry_fullname
    global entry_nickname

    with Session(engine) as session:
        if user := session.get(User, entry_user_id.get()):
            session.delete(user)
            session.commit()
        else:
            messagebox.showerror("L'id non è presente nel DB",
                                 "L'id non è presente nel DB", parent=root)
    popola_dati()


def export_to_csv():
    df = pt.model.df
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d-%H%M%S")
    df.to_csv(r"CSV_"+date_time+".csv", index=False, sep=";")


def aggiorna_testata():
    global riferimento_dettaglio
    global entry_user_id
    global entry_name
    global entry_fullname
    global entry_nickname

    entry_user_id.delete(0, 'end')
    entry_user_id.insert(0, riferimento_dettaglio[0])
    entry_name.delete(0, 'end')
    entry_name.insert(0, riferimento_dettaglio[1])
    entry_fullname.delete(0, 'end')
    entry_fullname.insert(0, riferimento_dettaglio[2])
    entry_nickname.delete(0, 'end')
    entry_nickname.insert(0, riferimento_dettaglio[3])


def main():
    global entry_generica
    global entry_user_id
    global entry_name
    global entry_fullname
    global entry_nickname

    global pt
    global root
    root = Tk()
    root.title("Gestione Underwater")
    root.geometry('1000x700+200+100')
    my_frame_top = ttk.Frame(root)
    my_frame_top.pack(pady=5, padx=5, fill=BOTH)

    my_frame_medio = ttk.Frame(root)
    my_frame_medio.pack(pady=5, padx=5, fill=BOTH)

    my_frame_comandi = ttk.Frame(root)
    my_frame_comandi.pack(pady=5, padx=5, fill=BOTH)

    my_frame_testata = ttk.Frame(root)
    my_frame_testata.pack(pady=5, padx=5, fill=BOTH)

    my_notebook = ttk.Notebook(root)
    my_notebook.pack(fill=BOTH, expand=1, pady=5, padx=5)
    my_frame_consegne_table = ttk.Frame(my_notebook)
    my_frame_consegne_table.pack(fill=BOTH, expand=1, pady=5, padx=5)
    my_notebook.add(my_frame_consegne_table, text="Gestione Underwater")

    my_btn_save = ttk.Button(
        my_frame_comandi, text="Salva dataframe in csv", command=export_to_csv)
    my_btn_save.pack(side="left", pady=5, padx=5)

    label_generica = ttk.Label(my_frame_top, text="Scelta ...")
    label_generica.pack(side="left", pady=5, padx=5)

    entry_generica = ttk.Entry(my_frame_top, width=10)
    entry_generica.pack(side="left", pady=5, padx=5)
    entry_generica.bind("<Return>", lambda event: popola_dati())
    entry_generica.insert(END, "Scelta...")
    # entry_deposito.bind('<Return>', dati_deposito)

    btn_generico = ttk.Button(
        my_frame_top, text="Aggiorna", command=popola_dati)
    btn_generico.pack(side="left", pady=5, padx=5)

    my_btn_save = ttk.Button(my_frame_comandi, text="Salva nel DB",
                             command=lambda: salva_utente_nel_db())
    my_btn_save.pack(side="left", pady=5, padx=5)

    my_btn_crea = ttk.Button(my_frame_comandi, text="Crea nel DB",
                             command=lambda: crea_utente_nel_db())
    my_btn_crea.pack(side="left", pady=5, padx=5)

    my_btn_cancella = ttk.Button(my_frame_comandi, text="Cancella dal DB",
                                 command=lambda: cancella_utente_dal_db())
    my_btn_cancella.pack(side="left", pady=5, padx=5)

    pt = Table(my_frame_consegne_table, showtoolbar=True, showstatusbar=True)

    label_user_id = ttk.Label(my_frame_testata, text="User id")
    label_user_id.pack(side="left", pady=5, padx=5)
    entry_user_id = ttk.Entry(my_frame_testata, width=10)
    entry_user_id.pack(side="left", pady=5, padx=5)
    label_name = ttk.Label(my_frame_testata, text="User Name")
    label_name.pack(side="left", pady=5, padx=5)
    entry_name = ttk.Entry(my_frame_testata, width=20)
    entry_name.pack(side="left", pady=5, padx=5)
    label_fullname = ttk.Label(my_frame_testata, text="User FullName")
    label_fullname.pack(side="left", pady=5, padx=5)
    entry_fullname = ttk.Entry(my_frame_testata, width=20)
    entry_fullname.pack(side="left", pady=5, padx=5)
    label_nickname = ttk.Label(my_frame_testata, text="User Nickname")
    label_nickname.pack(side="left", pady=5, padx=5)
    entry_nickname = ttk.Entry(my_frame_testata, width=20)
    entry_nickname.pack(side="left", pady=5, padx=5)
    btn_indirizzi = ttk.Button(
        my_frame_testata, text="Indirizzi", command=indirizzi_utente)
    btn_indirizzi.pack(side="left", pady=5, padx=5)

    def handle_left_click(event):
        global riferimento_dettaglio
        global df
        """Handle left click"""
        rowclicked_single = pt.get_row_clicked(event)
        colclicked_single = pt.get_col_clicked(event)
        # riferimento_dettaglio = df["ID"].iloc[[rowclicked_single]].values[0]
        riferimento_dettaglio = df.iloc[[rowclicked_single]].values[0]
        pt.setSelectedRow(rowclicked_single)
        aggiorna_testata()
        pt.redraw()

    pt.bind('<ButtonRelease-1>', handle_left_click)
    pt.autoResizeColumns()
    pt.show()

    root.mainloop()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
