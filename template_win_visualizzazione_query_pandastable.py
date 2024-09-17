import pyodbc
import pandas as pd
import datetime as dt
import numpy as np
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


def dettagli(riferimento_dettaglio):
    if riferimento_dettaglio:
        data_dettaglio = pd.to_datetime(
            riferimento_dettaglio[0]).strftime("%Y%m%d")
        num_dettaglio = riferimento_dettaglio[1]

        stringa_sql_esiti = f"""select data_sped, num_sped, COD_TRASPO, b.Desc2, data, ora  from sp_esiti a inner join sp_codesi b on a.cod_esito = b.cod_esito
        where data_sped = '{data_dettaglio}' and num_sped = '{num_dettaglio}'"""

        conn_string = os.environ.get("CONN_CARLI_TRUSTED")
        conn_esiti = pyodbc.connect(conn_string)
        df_dettaglio = pd.read_sql(stringa_sql_esiti, conn_esiti)
        if df_dettaglio.empty:
            messagebox.showinfo("Non ci sono dettagli",
                                "Non ci sono dettagli", parent=root)
        else:
            tabella = Toplevel(root)
            tabella.title("Tabella")
            # tabella.iconbitmap("Images/Icona.ico")
            tabella.geometry("1000x700")
            my_top_frame = ttk.Frame(tabella)
            my_top_frame.pack(fill=BOTH, expand=1, pady=5, padx=5)

            label_data_sped_lbl = ttk.Label(my_top_frame, text="Testata")
            label_data_sped_lbl.grid(row=0, column=0, pady=5, padx=5)
            label_data_sped_value = ttk.Label(my_top_frame, text="Placeholder")
            label_data_sped_value.grid(row=0, column=1, pady=5, padx=5)

            my_frame = ttk.Frame(tabella)
            my_frame.pack(fill=BOTH, expand=1, pady=5, padx=5)
            pt1 = Table(my_frame, showtoolbar=True, showstatusbar=True)
            pt1.model.df = df_dettaglio
            pt1.show()

        conn_esiti.close()
        # print(esiti)
    else:
        messagebox.showinfo("Non hai selezionato spedizioni",
                            "Non hai selezionato spedizioni", parent=root)


def popola_dati():
    global df
    deposito = entry_generica.get()
    stringa_sql = f"SELECT * FROM sp_sped where cod_deposito like '%{deposito}'"
    conn_string = os.environ.get("CONN_CARLI_TRUSTED")
    conn = pyodbc.connect(conn_string)
    df = pd.read_sql(stringa_sql, conn)
    conn.close()
    pt.model.df = df

    pt.redraw()

#df = table.model.df


def export_to_csv():
    df = pt.model.df
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d-%H%M%S")
    df.to_csv(r"CSV_"+date_time+".csv", index=False, sep=";")


def main():
    global entry_generica
    global pt
    global root
    root = Tk()
    root.title("Gestione file csv")
    root.geometry('1000x700+200+100')
    my_frame_top = ttk.Frame(root)
    my_frame_top.pack(pady=5, padx=5, fill=BOTH)

    my_frame_medio = ttk.Frame(root)
    my_frame_medio.pack(pady=5, padx=5, fill=BOTH)

    my_frame_comandi = ttk.Frame(root)
    my_frame_comandi.pack(pady=5, padx=5, fill=BOTH)

    my_notebook = ttk.Notebook(root)
    my_notebook.pack(fill=BOTH, expand=1, pady=5, padx=5)
    my_frame_consegne_table = ttk.Frame(my_notebook)
    my_frame_consegne_table.pack(fill=BOTH, expand=1, pady=5, padx=5)
    my_notebook.add(my_frame_consegne_table, text="Gestione file csv")

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

    my_btn_esiti = ttk.Button(my_frame_comandi, text="Visualizza Dettagli...",
                              command=lambda: dettagli(riferimento_dettaglio))
    my_btn_esiti.pack(side="left", pady=5, padx=5)

    pt = Table(my_frame_consegne_table, showtoolbar=True, showstatusbar=True)

    def handle_left_click(event):
        global riferimento_dettaglio
        global df
        riferimento_dettaglio = []
        """Handle left click"""
        rowclicked_single = pt.get_row_clicked(event)
        colclicked_single = pt.get_col_clicked(event)
        riferimento_dettaglio.append(
            df["DETTAGLIO"].iloc[[rowclicked_single]].values[0])

        pt.setSelectedRow(rowclicked_single)
        # print(riferimento_selezionato)
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
