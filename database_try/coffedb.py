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


@dataclass
class CoffeeProduct:
    id: int = 0
    name: str = ""
    price: float = 0

    def crea(self, conn):
        c = conn.cursor()
        c.execute("INSERT INTO coffee values (null, :name,:price)", self.__dict__)

    def aggiorna(self, conn):
        c = conn.cursor()
        c.execute(
            "UPDATE coffee set name = :name, price=:price where id=:id", self.__dict__
        )

    def leggi(self, conn):
        c = conn.cursor()
        c.execute(
            f"select id, name, price from coffee where id = :id", self.__dict__)
        return c

    def cancella(self, conn):
        c = conn.cursor()
        c.execute("DELETE from coffee where id=:id", self.__dict__)


id_da_utilizzare = 3


def crea_coffee(conn):
    coffee = CoffeeProduct(name="caffeina", price=10)
    # riga = print(coffee.__dict__)
    # riga = {"id": 12, "name": "kava", "price": 125}
    # c.execute("INSERT INTO coffe values (?,?,?)", coffe)
    # c.execute("INSERT INTO coffe values (:id,:name,:price)", coffee.__dict__)
    coffee.crea(conn)
    conn.commit()


def aggiorna_coffee(conn):
    coffee = CoffeeProduct(id=id_da_utilizzare, name="robusta", price=20)
    # riga = print(coffee.__dict__)
    # riga = {"id": 12, "name": "kava", "price": 125}
    # c.execute("INSERT INTO coffe values (?,?,?)", coffe)
    # c.execute("INSERT INTO coffe values (:id,:name,:price)", coffee.__dict__)
    coffee.aggiorna(conn)
    conn.commit()


def leggi_coffee(conn):
    coffee = CoffeeProduct(id=id_da_utilizzare)
    c = coffee.leggi(conn)
    # row = c.fetchone()
    # print(row.keys())
    for row in c.fetchall():
        coffee = CoffeeProduct(
            id=row["id"], name=row["name"], price=row["price"])
        print(coffee)
        # print(tuple(row))
        # print(row['id'], row['name'], row['price'])
        # print(f"(id = {row[0]} | nome = {row[1]} | kg = {row[2]})")
        # print(f"(id = {row['id']} | nome = {row['name']} | kg = {row['price']})")


def cancella_coffee(conn):
    coffee = CoffeeProduct(id=id_da_utilizzare)
    c = coffee.cancella(conn)
    conn.commit()


def main():
    conn = sqlite3.connect("coffee.db")
    conn.row_factory = sqlite3.Row

    try:
        crea_coffee(conn)
        leggi_coffee(conn)
        aggiorna_coffee(conn)
        leggi_coffee(conn)
        # cancella_coffee(conn)
        # leggi_coffee(conn)

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
