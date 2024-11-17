import datetime as dt
import os
from timeit import default_timer as timer

import holidays
import numpy as np
import pandas as pd

from servizio import log_setup

"""
Programma per calcolare il numero di giorni settimanali lavorativi che ci sono in ciascun mese dell'anno in corso.
Calcola il numero di lunedì, martedì ecc, non contandoli se sono festivi e poi stampa i risultati a video
e anche su un file excel se PROVA  = False
"""
start = timer()

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


def save_to_xlsx(df, year):
    with pd.ExcelWriter(
        rf"archivio/days_per_month_{year}.xlsx", engine="xlsxwriter"
    ) as writer:
        df.to_excel(writer, index=True, sheet_name=f"Giorni lavorativi {year}")
        # writer.save()


def main():
    today = dt.datetime.now()
    lista_giorni_mesi = []
    year = today.year
    calc_year = year
    next_calc_year = calc_year + 1
    list_hol = []
    for date, name in sorted(holidays.IT(years=calc_year).items()):
        list_hol.append([date, name])
    # Aggiungiamo San Giovanni ai giorni festivi
    date_san_gio = dt.datetime.strptime(
        f"24/06/{calc_year}", "%d/%m/%Y").date()
    festivita_carli = [date_san_gio, "San Giovanni"]
    list_hol.append(festivita_carli)
    list_hol.sort()

    for date in list_hol:
        print(date[0].strftime("%Y-%m-%d"), date[1])
    # Predispongo la lista del numero dei mesi in formato stringa
    months = [str(x).zfill(2) for x in range(1, 13)]

    week_days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    num_weekdays_year = 0
    for idx, month in enumerate(months):
        lista_colonna_mesi = []
        num_weekdays_month = 0
        print(
            f"----------------Month {month} Year {calc_year}--------------------")
        for week_day in week_days:
            # Predispongo le stringhe per passarle a busday_count nel formato AAAA-MM
            month_start = f"{calc_year}-{month}"
            if month == "12":
                month_next_start = f"{next_calc_year}-01"
            else:
                month_next_start = f"{calc_year}-{months[idx+1]}"

            num_single_weekday_month = np.busday_count(
                month_start,
                month_next_start,
                weekmask=week_day,
                holidays=[item[0] for item in list_hol],
            )
            lista_colonna_mesi.append(num_single_weekday_month)
            num_weekdays_month = num_weekdays_month + num_single_weekday_month

            print(
                f"Number of {week_day} in {month}-{calc_year}:",
                num_single_weekday_month,
            )

            if week_day == "Fri":
                print(
                    f"Total number of weekdays in {month}-{calc_year}: {num_weekdays_month}"
                )
        lista_giorni_mesi.append(lista_colonna_mesi)
        num_weekdays_year = num_weekdays_year + num_weekdays_month
    print(f"Total number of weekdays in {calc_year}: {num_weekdays_year}")
    arr_giorni = np.array(lista_giorni_mesi).T
    # print(arr_giorni)
    # df_giorni_mesi = pd.DataFrame(arr_giorni, columns=months, index=week_days)
    df_giorni_mesi = pd.DataFrame(arr_giorni, columns=months, index=week_days)
    # df_giorni_mesi = df_giorni_mesi.T
    # df_giorni_mesi.columns = months
    print(df_giorni_mesi)

    save_to_xlsx(df_giorni_mesi, calc_year)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        if PROVA:
            logger.info(e, exc_info=True)
        else:
            logger.critical(e, exc_info=True)

logger.info("Fine")

end = timer()
print("Elapsed Time: ", end - start)
