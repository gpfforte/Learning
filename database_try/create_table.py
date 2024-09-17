import sqlite3
from dataclasses import dataclass
from logging import DEBUG
from servizio import log_setup
import os
from time import perf_counter

start = perf_counter()

# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Setta il log
filename, _ = os.path.splitext(os.path.basename(__file__))
logger = log_setup.logging_setup(
    nomefile=filename, levelfile=DEBUG, name=__name__)

logger.info("Inizio")

PROVA = bool(os.environ.get("AMBIENTE_DI_PROVA") == "SI")


def crea_coffee_table(conn):
    c = conn.cursor()

    # c.execute("""DROP TABLE coffee""")

    c.execute(
        """CREATE table IF NOT EXISTS coffee (
        id integer PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price REAL
         )"""
    )

    conn.commit()


def main():
    conn = sqlite3.connect("coffee.db")
    # La riga seguente serve per far ritornare dizionari anziché tuple
    conn.row_factory = sqlite3.Row

    try:
        crea_coffee_table(conn)

    except Exception as e:
        if PROVA:
            logger.info(e, exc_info=True)
        else:
            logger.critical(e, exc_info=True)
    conn.close()


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
