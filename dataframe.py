from tkinter import *
from pandastable import Table, TableModel
import pandas as pd
import os
# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


class TestApp(Frame):
        """Basic test frame for the table"""
        def __init__(self, parent=None):
            self.parent = parent
            Frame.__init__(self)
            self.main = self.master
            self.main.geometry('800x600')
            self.main.title('Table app')
            f = Frame(self.main)
            f.pack(fill=BOTH,expand=1)
            # df = TableModel.getSampleData()
            self.df = pd.DataFrame({'importo': [0.25, 2.3, 3.4], 'prodotto': ['riga', 'cerchio', 'quadrato']})
            self.table = pt = Table(f, dataframe=self.df,
                                    showtoolbar=True, showstatusbar=True)
            self.btn=Button(self.main, text="Scarica csv",command=self.salva_csv)
            self.btn.pack()
            pt.show()
            # print(self.df["importo"])
            # self.df["importo"]=self.df["importo"].astype(str).str.replace(".", ",")
            # print(self.df["importo"])
            return
        def salva_csv(self):
            df_csv=self.df
            df_csv["importo"]=df_csv["importo"].astype(str).str.replace(".", ",")
            df_csv.to_csv("dataframe_prova_conv_punti_decimali.csv", index=False, sep=";")



app = TestApp()
#launch the app
app.mainloop()