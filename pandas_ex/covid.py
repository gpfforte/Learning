import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from logging import DEBUG
import datetime as dt
from servizio import log_setup
import os
from time import perf_counter
import os
import pandas as pd

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


def main():
    # %matplotlib inline
    # %matplotlib notebook

    df = pd.read_csv(
        "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv"
    )

    pd.set_option("display.max_rows", 500)
    pd.set_option("display.max_columns", 500)
    pd.set_option("display.width", 200)

    # df["perc_positivi"]=df["nuovi_positivi"]/df["casi_testati"]*100
    # print(df.columns)
    filt = df["data"] >= "2022-01-01T00:00:00"
    df1 = df.loc[filt]
    df1["nuovi_deceduti"] = df1["deceduti"] - df1["deceduti"].shift(1)
    df1["tamponi_effettuati"] = df1["tamponi"] - df1["tamponi"].shift(1)
    df1["perc_positivi"] = df1["nuovi_positivi"] / \
        df1["tamponi_effettuati"] * 100

    # print(df1.head())
    # print(df1.tail())
    print(df1.describe())
    print(df1.dtypes)
    print(df1.head())
    print(df1.tail())
    print(df1.shape)
    df1.to_csv("covid.csv", sep=";")

    # print (df["totale_positivi"])
    # Occorre fare dei subplot per via delle scale diverse
    fig, axs = plt.subplots(2, 2)
    axs[0, 0].plot(df1["data"], df1["totale_positivi"])
    axs[0, 0].set_title("Totale positivi")
    axs[1, 0].plot(df1["data"], df1["terapia_intensiva"])
    axs[1, 0].set_title("Terapia intensiva")
    axs[0, 1].plot(df1["data"], df1["nuovi_deceduti"])
    axs[0, 1].set_title("Nuovi deceduti")
    axs[1, 1].plot(df1["data"], df1["perc_positivi"])
    axs[1, 1].set_title("Percentuale nuovi positivi")
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
