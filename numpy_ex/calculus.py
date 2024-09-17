from logging import DEBUG
from datetime import datetime, timedelta
from tkinter import Label

from numpy.core.shape_base import vstack
from servizio import log_setup
import os
from time import perf_counter
import os
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

start = perf_counter()
# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Setta il log
filename, _ = os.path.splitext(os.path.basename(__file__))
logger = log_setup.logging_setup(
    nomefile=filename, levelfile="DEBUG", name=__name__)
logger.info("Inizio")

PROVA = bool(os.environ.get("AMBIENTE_DI_PROVA") == "SI")

df = pd.DataFrame()


def main():
    x = np.linspace(-10, 10, 20)
    y = x**2 - 1
    # Calcolo derivata
    dydx = np.gradient(y, x)
    # print(dydx)
    # Calcolo integrale, ovviamente si può aggiungere qualsiasi costante, che in questo caso
    # è il primo punto della somma
    inty = np.cumsum(y) * (x[1] - x[0])
    # Calcolo la derivata dell'integrale per vedere se mi torna la funzione iniziale, si vede
    # che man mano che l'intervalle diventa più piccolo si avvicina sempore di più alla funzione iniziale
    # per vederlo basta aumentare o diminuire il numero dei punti nella funzione linspace
    d_inty = np.gradient(inty, x)
    plt.plot(x, y, label="y")
    plt.plot(x, dydx, label="dydx")
    plt.plot(x, inty, label="inty")
    plt.plot(x, d_inty, label="d_inty")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        if PROVA:
            logger.info(e, exc_info=True)
        else:
            logger.critical(e, exc_info=True)
logger.info("Fine")
end = perf_counter()
print("Elapsed Time: ", end - start)
