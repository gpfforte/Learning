import datetime as dt
import tkinter.font as tkFont
from tkinter import (BOTH, END, LEFT, TOP, Entry, Label, LabelFrame, Listbox,
                     StringVar, Tk, W, messagebox, ttk)

import pandas as pd
from pandastable import Table, TableModel
from tkcalendar import Calendar, DateEntry

from servizio.funzioni_servizio import export_to_csv

# Calcoliamo che giorno è oggi
today = dt.datetime.now()


class ControlloDataBase:
    """
    Classe per facilitare accesso al Database passando:
    * una stringa con codice sql ed eventuali placeholder per data inizio e fine
    * engine per connessione
    * logger
    * data_inizio
    * data_fine
    * nomefile da dare al file dei risultati
    """

    def __init__(
        self, stringa_sql, engine, logger, data_inizio, data_fine, nomefile, salva_file=True
    ) -> None:
        self.stringa_sql = stringa_sql
        self.engine = engine
        self.logger = logger
        self.nomefile = nomefile
        self.data_inizio = data_inizio
        self.data_fine = data_fine
        self.popola_dati()
        # print(salva_file)
        if salva_file is None:
            self.salva_file = True
        else:
            self.salva_file = salva_file
        if self.salva_file:
            self.filename_timestamp = export_to_csv(
                logger=self.logger, df=self.df, nomefile=self.nomefile
            )

    def popola_dati(self):
        self.logger.debug(f"data_inizio = {self.data_inizio}")
        self.logger.debug(f"data_fine = {self.data_fine}")
        self.logger.debug("popola_dati iniziata")
        with self.engine.connect() as conn:
            self.df = pd.read_sql(
                self.stringa_sql.format(
                    data_inizio=self.data_inizio, data_fine=self.data_fine
                ),
                conn,
            )
        self.logger.debug(f"len(df) = {len(self.df)}")

    def __str__(self):
        return f"""
        Controllo con stringa:
        '{self.stringa_sql.format(
                    data_inizio=self.data_inizio, data_fine=self.data_fine
                )}'
        """


class MyTab:
    """
    Prepara un frame con dentro un tab (occorre passare un notebook), con una dropdown per scegliere la nazione,
    una data di inizio, una data fine (fatte con DateEntry) e un pulsante per aggiornare su una riga.
    Alcuni radiobutton per selezionare intervalli predefiniti nelle date inizio e fine.
    E' presente anche un pulsante per salvare il dataframe mostrato nella tabella con il nome del tab
    ed il timestamp.
    Sono previsti ulteriori radiobutton per alcune tipologie di raggruppamento eventualmente previsite.
    Questi radiobutton si possono personalizzare per mostrare quelli che si vogliono, tramite
    una tupla.
    Esempio di chiamata:
    radio_tupla_ordini = ("Totali",
                          "Totali per Nazione-Data Immissione",
                          "Totali per Nazione-Tipo Immissione",
                          "Totali per Nazione-Pagamento",
                          "Stato",
                          "No Totali")
    tab_ordini = MyTab(my_notebook, "ORDINI", radio_tupla_ordini)
    """

    def __init__(self, my_notebook, tab_name, radio_tupla, table=True) -> None:
        self.data_inizio_prev = ""
        self.data_fine_prev = ""
        self.df1 = pd.DataFrame()
        self.df2 = pd.DataFrame()
        self.df3 = pd.DataFrame()
        self.df_no_group = pd.DataFrame()
        self.tab_name = tab_name
        self.frame_tab = ttk.Frame(my_notebook, borderwidth=1, relief="groove")
        self.frame_tab.pack(fill=BOTH, expand=1, pady=5, padx=5, anchor="n")
        my_notebook.add(self.frame_tab, text=self.tab_name)

        self.frame_top = ttk.Frame(
            self.frame_tab, borderwidth=1, relief="groove")
        self.frame_top.pack(pady=5, padx=5, fill=BOTH)
        self.label_nazione = ttk.Label(self.frame_top, text="Nazione")
        self.label_nazione.pack(side="left", pady=5, padx=5)
        self.scelta_nazione = StringVar()
        self.combo_nazione = ttk.Combobox(
            self.frame_top,
            textvariable=self.scelta_nazione,
            values=["", "ITA", "DEU", "FRA", "AUT", "CHE", "BEL"],
            width=10,
            state="readonly",
        )
        self.combo_nazione.pack(side="left", pady=5, padx=5)
        self.combo_nazione.current(newindex=0)

        self.frame_timeframe = ttk.Frame(
            self.frame_tab, borderwidth=1, relief="groove")
        self.frame_timeframe.pack(pady=5, padx=5, fill=BOTH)

        self.frame_comandi = ttk.Frame(
            self.frame_tab, borderwidth=1, relief="groove")
        self.frame_comandi.pack(pady=5, padx=5, fill=BOTH)
        self.frame_medio = ttk.Frame(
            self.frame_tab, borderwidth=1, relief="groove")
        self.frame_medio.pack(pady=5, padx=5, fill=BOTH)
        self.frame_radio = LabelFrame(
            self.frame_tab, text="Modalità", borderwidth=1, relief="groove"
        )
        self.frame_radio.pack(pady=5, padx=5, fill=BOTH)
        self.frame_data = ttk.Frame(
            self.frame_tab, borderwidth=1, relief="groove")
        self.frame_data.pack(pady=5, padx=5, expand=True, fill=BOTH, side=TOP)
        self.frame_table = ttk.Frame(
            self.frame_tab, borderwidth=1, relief="groove")
        self.frame_table.pack(pady=5, padx=5, expand=True, fill=BOTH, side=TOP)

        if table:
            self.pt = Table(self.frame_table, showtoolbar=True,
                            showstatusbar=True)
        else:
            self.my_treeview = MyTreeview(self.frame_table)
            # self.my_listbox.pack(
            #     pady=5, padx=5, expand=True, fill=BOTH, side=TOP)
        self.btn_save = ttk.Button(
            self.frame_comandi,
            text="Salva dataframe in csv",
            command=lambda: self.export_to_csv(),
        )
        self.btn_save.pack(side="left", pady=5, padx=5)

        self.label_inizio = ttk.Label(self.frame_top, text="Data Inizio")
        self.label_inizio.pack(side="left", pady=5, padx=5)
        self.cal_inizio = DateEntry(
            self.frame_top,
            width=12,
            background="grey",
            foreground="white",
            borderwidth=2,
            locale="it_IT",
            date_pattern="YYYY-MM-DD",
            year=today.year,
            month=today.month,
            day=today.day,
        )
        self.cal_inizio.pack(side="left", padx=5, pady=5)

        self.label_fine = ttk.Label(self.frame_top, text="Data Fine")
        self.label_fine.pack(side="left", pady=5, padx=5)
        self.cal_fine = DateEntry(
            self.frame_top,
            width=12,
            background="grey",
            foreground="white",
            borderwidth=2,
            locale="it_IT",
            date_pattern="YYYY-MM-DD",
            year=today.year,
            month=today.month,
            day=today.day,
        )
        self.cal_fine.pack(side="left", padx=5, pady=5)

        self.var_timeframe = StringVar()
        self.rtoday = ttk.Radiobutton(
            self.frame_timeframe,
            text="Today",
            variable=self.var_timeframe,
            value="Today",
            command=lambda: self.update_dates("Today"),
        )
        self.rtoday.pack(side="left", pady=5, padx=5)
        self.ryesterday = ttk.Radiobutton(
            self.frame_timeframe,
            text="Yesterday",
            variable=self.var_timeframe,
            value="Yesterday",
            command=lambda: self.update_dates("Yesterday"),
        )
        self.ryesterday.pack(side="left", pady=5, padx=5)
        self.rlastweek = ttk.Radiobutton(
            self.frame_timeframe,
            text="Lastweek",
            variable=self.var_timeframe,
            value="Lastweek",
            command=lambda: self.update_dates("Lastweek"),
        )
        self.rlastweek.pack(side="left", pady=5, padx=5)
        self.rlastmonth = ttk.Radiobutton(
            self.frame_timeframe,
            text="Lastmonth",
            variable=self.var_timeframe,
            value="Lastmonth",
            command=lambda: self.update_dates("Lastmonth"),
        )
        self.rlastmonth.pack(side="left", pady=5, padx=5)
        self.rlast2month = ttk.Radiobutton(
            self.frame_timeframe,
            text="Last 2 months",
            variable=self.var_timeframe,
            value="Last2months",
            command=lambda: self.update_dates("Last2months"),
        )
        self.rlast2month.pack(side="left", pady=5, padx=5)
        self.rlastyear = ttk.Radiobutton(
            self.frame_timeframe,
            text="Lastyear",
            variable=self.var_timeframe,
            value="Lastyear",
            command=lambda: self.update_dates("Lastyear"),
        )
        self.rlastyear.pack(side="left", pady=5, padx=5)

        self.rtoday.invoke()
        self.radio_mode = []
        self.var_mode = StringVar()
        for item in radio_tupla:
            radio_tmp = ttk.Radiobutton(
                self.frame_radio, text=item, variable=self.var_mode, value=item
            )
            radio_tmp.pack(side="left", pady=5, padx=5)
            self.radio_mode.append(radio_tmp)

        if self.radio_mode:
            self.radio_mode[0].invoke()
        if table:
            self.pt.autoResizeColumns()
            self.pt.show()

    def export_to_csv(self):
        try:
            df = self.pt.model.df
        except Exception:
            df = self.my_treeview.df_data
        if not (df.empty):
            now = dt.datetime.now()
            date_time = now.strftime("%Y-%m-%d-%H%M%S")
            df.to_csv(
                rf'archivio/CSV_{self.tab_name.replace(" ", "_")}_{date_time}.csv',
                index=False,
                sep=";",
                decimal=",",
                encoding="UTF-8",
            )
        else:
            messagebox.showinfo(
                "Dataframe vuoto",
                "Non ci sono dati da esportare",
                parent=self.frame_tab,
            )

    def update_dates(self, interval):
        if interval == "Today":
            self.cal_inizio.set_date(today)
            self.cal_fine.set_date(today)
        elif interval == "Yesterday":
            delta_indietro = dt.timedelta(days=1)
            yesterday = today - delta_indietro
            self.cal_inizio.set_date(yesterday)
            self.cal_fine.set_date(yesterday)
        elif interval == "Lastweek":
            delta_indietro = dt.timedelta(days=7)
            lastweek = today - delta_indietro
            delta_indietro = dt.timedelta(days=1)
            yesterday = today - delta_indietro
            self.cal_inizio.set_date(lastweek)
            self.cal_fine.set_date(yesterday)
        elif interval == "Lastmonth":
            first_thismonth = today.replace(day=1)
            last_lastMonth = first_thismonth - dt.timedelta(days=1)
            first_lastmonth = last_lastMonth.replace(day=1)
            self.cal_inizio.set_date(first_lastmonth)
            self.cal_fine.set_date(last_lastMonth)
        elif interval == "Last2months":
            first_thismonth = today.replace(day=1)
            last_lastMonth = first_thismonth - dt.timedelta(days=1)
            first_lastmonth = last_lastMonth.replace(day=1)
            last_previousMonth = first_lastmonth - dt.timedelta(days=1)
            first_previousMonth = last_previousMonth.replace(day=1)
            self.cal_inizio.set_date(first_previousMonth)
            self.cal_fine.set_date(last_lastMonth)
        elif interval == "Lastyear":
            first_lastyear = today.replace(day=1, month=1, year=today.year - 1)
            last_lastyear = today.replace(
                day=31, month=12, year=today.year - 1)
            self.cal_inizio.set_date(first_lastyear)
            self.cal_fine.set_date(last_lastyear)


class MyTreeview:
    """use a ttk.TreeView as a multicolumn ListBox
    You can pass data directly or pass them with update_data method
    You can also pass a function to bind to the selection event"""

    def __init__(self, parent, df_data=None, bind_func=None):
        self.df_data = pd.DataFrame() if df_data is None else df_data
        self.tree = None
        self.parent = parent
        self.frame_container = ttk.Frame(self.parent)
        self.frame_container.pack(
            fill="both", expand=True, padx=5, pady=5, side="top")
        self.bind_func = bind_func
        self._apply_style()
        self._setup_widgets()
        self._build_columns()
        self._fill_tree()

    def _setup_widgets(self):
        # create a treeview with dual scrollbars
        columns = list(self.df_data.columns)
        self.tree = ttk.Treeview(
            self.frame_container, columns=columns, show="headings", selectmode="browse"
        )
        # print(columns)
        vsb = ttk.Scrollbar(
            self.frame_container, orient="vertical", command=self.tree.yview
        )
        hsb = ttk.Scrollbar(
            self.frame_container, orient="horizontal", command=self.tree.xview
        )
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky="nsew")
        vsb.grid(column=1, row=0, sticky="ns")
        hsb.grid(column=0, row=1, sticky="ew")
        self.frame_container.grid_columnconfigure(0, weight=1)
        self.frame_container.grid_rowconfigure(0, weight=1)
        self.tree.tag_configure("oddrow", background="white")
        self.tree.tag_configure("evenrow", background="lightgrey")
        self.tree.bind("<<TreeviewSelect>>", self.bind_func)

    def _build_columns(self):
        for col in self.df_data.columns:
            # print(col)
            self.tree.heading(
                col,
                text=col.title(),
                command=lambda col=col: self.sortby(self.tree, col, 0),
            )
            # adjust the column's width to the header string
            self.tree.column(col, width=tkFont.Font().measure(
                col.title()), minwidth=30)

    def _fill_tree(self):
        self.count_rows = 0
        for _, item in self.df_data.iterrows():
            dato = [x[1] for x in list(item.items())]
            tag = ("evenrow",) if self.count_rows % 2 == 0 else ("oddrow",)
            self.tree.insert("", "end", values=dato, tag=tag)
            # adjust column's width if necessary to fit each value
            for ix, val in enumerate(dato):
                if val is None:
                    col_w = 18
                else:
                    col_w = tkFont.Font().measure(val)
                if self.tree.column(self.df_data.columns[ix], width=None) < col_w:
                    self.tree.column(self.df_data.columns[ix], width=col_w)
            self.count_rows += 1

    def sortby(self, tree, col, descending):
        """sort tree contents when a column header is clicked on"""
        self.df_data = self.df_data.sort_values(
            by=col, axis=0, ascending=descending)
        # # grab values to sort
        # data = [(tree.set(child, col), child)
        #         for child in tree.get_children('')]
        # # if the data to be sorted is numeric change to float
        # #data =  change_numeric(data)
        # # now sort the data in place
        # data.sort(reverse=descending)
        # for ix, item in enumerate(data):
        #     tree.move(item[1], '', ix)
        # # switch the heading so it will sort in the opposite direction
        tree.heading(
            col, command=lambda col=col: self.sortby(
                tree, col, int(not descending))
        )
        self.tree.delete(*tree.get_children())
        self._fill_tree()

    def _apply_style(self):
        style = ttk.Style()
        style.theme_use("clam")  # alt clam classic default vista
        style.configure(
            "Treeview", background="#D3D3D3", rowheight=25, fieldbackground="#D3D3D3"
        )
        style.map("Treeview", background=[("selected", "#324a6e")])

    def update_data(self, df_data):
        self.df_data = df_data
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = ()
        # columns = list(self.df_data.columns)
        # self.tree = ttk.Treeview(
        #     self.frame_container, columns=columns, show="headings")
        # self.tree.grid(column=0, row=0, sticky='nsew')
        self._setup_widgets()
        self._build_columns()
        self._fill_tree()


class MyFieldDesc:
    """
    Class to define an oject with description and value that can be "packed" on a GUI.
    It has an update method to simplify the substitution of text in an entry
    """

    def __init__(self, parent, desc):
        self.label = Label(parent, text=desc)
        self.label.pack(side="left", pady=5, padx=5)
        self.entry = Entry(parent, width=10)
        self.entry.pack(side="left", pady=5, padx=5)

    def update_value(self, text):
        self.entry.delete(0, END)
        self.entry.insert(0, text)
