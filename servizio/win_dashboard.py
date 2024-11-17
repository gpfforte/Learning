from tkinter import Tk, BOTH
from tkinter import ttk
import os

# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


def situazione_consegne():
    os.system('python ../Situazione_Consegne/win_situazione_consegne.py')


def situazione_consegne_storico():
    os.system('python ../Situazione_Consegne/win_leggi_db_situazione_consegne.py')


def consegne_chiuse():
    os.system('python ../Situazione_Consegne/win_consegne_chiuse.py')


def consegne_chiuse_no_prev():
    os.system('python ../Situazione_Consegne/win_consegne_chiuse_no_prev.py')


root = Tk()
root.title("Dashboard")
root.geometry('800x600+200+100')

my_frame_top = ttk.Frame(root)
my_frame_top.pack(pady=5, padx=5, fill=BOTH)

my_btn_situazione_consegne = ttk.Button(
    my_frame_top, text="Situazione Consegne", command=situazione_consegne)
my_btn_situazione_consegne.pack(side="left", pady=5, padx=5)

my_btn_situazione_consegne_storico = ttk.Button(
    my_frame_top, text="Storico Situazione Consegne", command=situazione_consegne_storico)
my_btn_situazione_consegne_storico.pack(side="left", pady=5, padx=5)

my_btn_consegne_chiuse = ttk.Button(
    my_frame_top, text="Consegne Chiuse", command=consegne_chiuse)
my_btn_consegne_chiuse.pack(side="left", pady=5, padx=5)

my_btn_consegne_chiuse_no_prev = ttk.Button(
    my_frame_top, text="Consegne Chiuse Senza Previsione", command=consegne_chiuse_no_prev)
my_btn_consegne_chiuse_no_prev.pack(side="left", pady=5, padx=5)

root.mainloop()
