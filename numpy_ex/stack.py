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
print(df.shape)


def graph():
    X = np.linspace(-2 * np.pi, 2 * np.pi, 1000)
    Y = np.cos(X)
    Z = np.sin(X)
    plt.style.use("seaborn")

    # plt.xticks(rotation=70)
    # plt.title("Grafico")
    fig, (ax1, ax2) = plt.subplots(2, 1)
    ax1.plot(X, Y, label="Coseno")
    ax1.set_title("Coseno")
    ax1.text(
        0.03,
        0.03,
        "Grafico del Coseno",
        fontsize="small",
        fontstyle="italic",
        transform=ax1.transAxes,
    )
    ax1.legend()
    ax2.text(
        0.90,
        0.82,
        "Grafico del Seno",
        fontsize="small",
        fontstyle="italic",
        transform=ax2.transAxes,
    )
    ax2.plot(X, Z, label="Seno")
    ax2.set_title("Seno")
    ax2.legend()
    plt.tight_layout()
    plt.show()


def main():
    a = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]).reshape(2, 5)
    print(a)
    a1 = np.array([[1, 1], [2, 2]])
    a2 = np.array([[3, 3], [4, 4]])
    print(np.vstack((a1, a2)))
    print(np.hstack((a1, a2)))
    graph()


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
