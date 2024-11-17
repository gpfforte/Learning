from logging import DEBUG
from servizio import log_setup
import os
from time import perf_counter, strftime, strptime
import os
import pandas as pd
import os
import numpy as np
import holidays
import datetime as dt


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


today = dt.datetime.now()
year = today.year
year_list = [year, year + 1]
list_hol = []
for anno in year_list:
    for date, name in sorted(holidays.IT(years=anno).items()):
        list_hol.append([date, name])
        # Aggiungiamo San Giovanni ai giorni festivi
        date_san_gio = dt.datetime.strptime(f"24/06/{anno}", "%d/%m/%Y").date()
        festivita_carli = [date_san_gio, "San Giovanni"]
        list_hol.append(festivita_carli)
list_hol.sort()


def add_working_days(x):
    # X[0]=data di partenza, X[1] giorni da aggiungere
    """
    Funzione che calcola una data aggiungendo dei giorni lavorativi ad una data iniziale, considera
    come giorno anche quello iniziale se è lavorativo.
    """

    days_elapsed = 0
    test_date = x[0]
    while days_elapsed < x[1]:
        test_date = test_date + dt.timedelta(days=1)
        if test_date.weekday() > 5 or test_date in [item[0] for item in list_hol]:
            # if a sunday or holiday skip
            continue
        else:
            # if a workday, count as a day
            days_elapsed += 1
    return test_date


def add_business_days(data_inizio, giorni_da_aggiungere):
    """
    Funzione che calcola una data aggiungendo dei giorni lavorativi ad una data iniziale, considera
    come giorno anche quello iniziale se è lavorativo. Meno performate rispetto a add_working_days
    """
    giorni_prova = giorni_da_aggiungere
    while True:
        data_prova = data_inizio + dt.timedelta(days=float(giorni_prova))
        giorni_business = np.busday_count(
            data_inizio,
            data_prova,
            weekmask="1111110",
            holidays=[item[0] for item in list_hol],
        )

        if (
            data_prova not in [item[0] for item in list_hol]
            and data_prova.weekday() < 6
        ):
            giorni_business = giorni_business + 1
        if (
            data_inizio not in [item[0] for item in list_hol]
            and data_inizio.weekday() < 6
        ):
            giorni_business = giorni_business - 1
        giorni_prova += 1
        if giorni_business >= giorni_da_aggiungere:
            break
    return data_prova


def main():
    date = dt.datetime.now().date()
    print(type(today.date()))
    # date = dt.datetime.strptime(
    #     "2021-12-25", '%Y-%m-%d').date()  # strptime("2021-12-25")
    for i in range(366):
        data_fine = add_working_days([date, i])
        # data_fine = add_business_days(date, i)
        print("Giorni da aggiungere", i, data_fine)


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
