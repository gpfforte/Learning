import datetime as dt
import os
import shutil
from logging import DEBUG
from time import perf_counter

import pandas as pd
import pyodbc

from servizio import log_setup
from servizio.funzioni_servizio import invio_email

start = perf_counter()
PROVA = bool(os.environ.get("AMBIENTE_DI_PROVA") == "SI")

# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Setta il log
filename, _ = os.path.splitext(os.path.basename(__file__))
logger = log_setup.logging_setup(
    nomefile=filename, levelfile=DEBUG, name=__name__)

logger.info("Inizio")


# data_inizio_prev = ""
# data_fine_prev = ""
conn_string = os.environ.get("CONN_CARLIBASE_TRUSTED")

destinatari = "g.forte@oliocarli.it"


def popola_dati(giorni_indietro):
    logger.info("popola_dati iniziata")

    conn = pyodbc.connect(conn_string)
    stringa_sql = f"""SELECT [IMPORTO],b.NUM_ORD_SF, b.COD_CLIENTE, b.OP_ID_IMM, b.NOMINATIVO
                    FROM [CARLIBASE].[SF].[RETSCO] a inner join [CARLIBASE].[SF].ORDINI b
                    on a.ID_ORDINE_SF=b.ID_ORDINE_SF
                    where (a.IMPORTO = 10 or a.IMPORTO = 15)
                    and a.COD_PROMOZIONE = ''
                    and b.DATA_ORA_IMM >= getdate() - {giorni_indietro} 
                    and b.NAZ='ITA'
                    and b.TIPO_IMM='T'
                    order by b.DATA_ORA_IMM
                """  # '2022-01-01 00:00:00'

    df = pd.read_sql(stringa_sql, conn)
    # logger.debug("df : "+ df.head())
    logger.info("popola_dati terminata")
    return df


def export_to_csv(df):
    logger.info("export_to_csv iniziata")
    now = dt.datetime.now()
    date_time = now.strftime("%Y-%m-%d-%H%M%S")
    path = f"CSV_Ordini_Promo_da_Controllare_{date_time}.csv"
    df.to_csv(path, index=False, sep=";")
    logger.info("export_to_csv terminata")
    return path


def main():
    giorni_indietro = 7
    try:
        df = popola_dati(giorni_indietro)
        filename = export_to_csv(df)
        invio_email(
            logger,
            filename=filename,
            destinatari=destinatari,
            soggetto="Ordini Promo da Controllare",
            contenuto="Ordini da controllare, vedi allegato.",
        )
        shutil.move(filename, f"archivio/{filename}")
    except Exception as e:
        if PROVA:
            logger.info(e, exc_info=True)
        else:
            logger.critical(e, exc_info=True)
    # Altro codice


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        if PROVA:
            logger.info(e, exc_info=True)
        else:
            logger.critical(e, exc_info=True)

end = perf_counter()

logger.info(f"Fine - Elapsed Time: {end - start}")


print("Elapsed Time: ", end - start)
