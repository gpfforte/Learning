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
from servizio.classi import MyTreeview

# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
df = pd.DataFrame()


def popola_dati(my_treeview):
    global df
    stringa_sql = """select tp.COD_TP, z.ZONA, min(p.DATA_SPED) as PROSSIMA_SPEDIZIONE from [DIST].[TRANSITPOINT] tp join [CARLIBASE].[SPED].[PIANO] p on p.ID_TP = tp.id join [CARLIBASE].[SPED].[PIANO_DETTAGLIO] pd on pd.ID_PIANO=p.id join [DIST].[ZONA] z on pd.ID_ZONA = z.id
                    where p.DATA_SPED >= GETDATE() and tp.COD_TP not in ('04', '3B', '3D', '36')
                    group by tp.COD_TP, z.zona
                    order by tp.COD_TP, z.zona"""
    conn_string = os.environ.get("CONN_CARLIBASE_TRUSTED")
    conn = pyodbc.connect(conn_string)
    df = pd.read_sql(stringa_sql, conn)
    conn.close()
    my_treeview.update_data(df)


def export_to_csv():
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d-%H%M%S")
    df.to_csv(r"CSV_"+date_time+".csv", index=False, sep=";")


def popola(event):
    item = my_treeview.tree.set(my_treeview.tree.focus())
    cod_tp = str(item["COD_TP"])
    zona = str(item["ZONA"])
    prossima_spedizione = str(item["PROSSIMA_SPEDIZIONE"])
    print(cod_tp, zona, prossima_spedizione)


def main():
    global my_treeview
    global root
    root = Tk()
    root.title("Gestione file csv")
    root.geometry('1000x700+200+100')
    style = ttk.Style()
    style.theme_use("clam")
    style.configure('Emergency.TButton', font='helvetica 12', foreground='red',
                    background='yellow', padding=5)
    style.map('Emergency.TButton',
              foreground=[('pressed', 'blue'),
                          ('active', 'yellow')],
              background=[('pressed', 'green'),
                          ('active', 'red')])

    def chiudi():
        root.destroy()
    my_frame_top = ttk.Frame(root)
    my_frame_top.pack(pady=5, padx=5, fill=BOTH)

    my_notebook = ttk.Notebook(root)
    my_notebook.pack(fill=BOTH, expand=1, pady=5, padx=5)
    my_frame_consegne_table = ttk.Frame(my_notebook)
    my_frame_consegne_table.pack(fill=BOTH, expand=1, pady=5, padx=5)
    my_notebook.add(my_frame_consegne_table,
                    text="Gestione data di Spedizione")
    my_treeview = MyTreeview(my_frame_consegne_table, bind_func=popola)
    btn_chiudi = ttk.Button(my_frame_top, text="Chiudi",
                            command=chiudi, style="Emergency.TButton")
    btn_chiudi.pack(side="left", pady=10, padx=10)
    btn_generico = ttk.Button(
        my_frame_top, text="Aggiorna", command=lambda: popola_dati(my_treeview))
    btn_generico.pack(side="left", pady=5, padx=5)

    # my_btn_esiti = ttk.Button(my_frame_comandi, text="Visualizza Dettagli...",
    #                           command=lambda: dettagli(riferimento_dettaglio))
    # my_btn_esiti.pack(side="left", pady=5, padx=5)

    # pt = Table(my_frame_consegne_table, showtoolbar=True, showstatusbar=True)

    # def handle_left_click(event):
    #     global riferimento_dettaglio
    #     global df
    #     riferimento_dettaglio = []
    #     """Handle left click"""
    #     rowclicked_single = pt.get_row_clicked(event)
    #     colclicked_single = pt.get_col_clicked(event)
    #     riferimento_dettaglio.append(
    #         df["DETTAGLIO"].iloc[[rowclicked_single]].values[0])

    #     pt.setSelectedRow(rowclicked_single)
    #     # print(riferimento_selezionato)
    #     pt.redraw()

    # pt.bind('<ButtonRelease-1>', handle_left_click)
    # pt.autoResizeColumns()
    # pt.show()

    root.mainloop()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
