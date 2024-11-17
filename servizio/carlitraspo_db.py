import os
from logging import DEBUG
from time import perf_counter

from sqlalchemy import Column, DateTime, MetaData, String, Table
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import registry

from servizio import log_setup
from servizio.connessioni import engine_carlitraspo, session_carlitraspo

# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Setta il log
filename, _ = os.path.splitext(os.path.basename(__file__))
logger = log_setup.logging_setup(nomefile=filename, levelfile=DEBUG, name=__name__)

PROVA = bool(os.environ.get("AMBIENTE_DI_PROVA") == "SI")
metadata = MetaData()
"""
TARIFFE_ZONE_DEP_REPORT è una view e per poterla mappare è stato necessario costruire una Table per definire la primary key, altrimenti non la rilevava.
Successivamente, per poter definire uno str method ho dovuto definire una class Tariffe da non far ereditare da base ne da autobase e fare un map_imperatively
tra la classe definita e la Table. In questo modo l'oggetto Tariffe è possibile trattarlo come se rappresentasse la definizione di una base o di una autobase
"""
lista_tabelle = [
    "SP_SPED",
    "SP_SPED1",
    "SP_DEPOSITI",
    "SP_INCASSI",
    "SP_TRASPO",
    "SP_ARTMGZ",
    "SP_ESITI",
    "UT_TRASPO",
    "TARIFFE_ZONE_DEP_REPORT",
]
metadata.reflect(engine_carlitraspo, only=lista_tabelle, views=True)

BaseAuto = automap_base(metadata=metadata)
BaseAuto.prepare()
mapper_registry = registry()
tariffe = Table(
    "TARIFFE_ZONE_DEP_REPORT",
    mapper_registry.metadata,
    Column("zona", String, primary_key=True),
    Column("cod_deposito", String, primary_key=True),
    Column("data_inizio_valid", DateTime, primary_key=True),
    Column("data_fine_valid", DateTime, primary_key=True),
    autoload=True,
    autoload_with=engine_carlitraspo,
    extend_existing=True,
)


class Tariffe:
    def __str__(self):
        return f"{self.cod_deposito}-{self.zona}-{self.data_inizio_valid}-{self.data_fine_valid}-{self.TARIFFA}"


mapper_registry.map_imperatively(Tariffe, tariffe)

Sp_Sped = BaseAuto.classes.SP_SPED
Sp_Sped1 = BaseAuto.classes.SP_SPED1
Sp_Incassi = BaseAuto.classes.SP_INCASSI
Sp_Esiti = BaseAuto.classes.SP_ESITI
Sp_Artmgz = BaseAuto.classes.SP_ARTMGZ
Sp_Depositi = BaseAuto.classes.SP_DEPOSITI
Ut_Traspo = BaseAuto.classes.UT_TRASPO


def main():
    start = perf_counter()
    with session_carlitraspo:
        for item in BaseAuto.classes:
            print(item)

    for table in BaseAuto.metadata.sorted_tables:
        # print(dir(table))
        print(f"Tabella: {table.name}")
        for c in table.columns:
            # print('')
            print(f"Colonna: {c}")
        for primary_key in table.primary_key:
            print(f"Primary Key: {primary_key}")
        for fkey in table.foreign_keys:
            print(fkey)
    end = perf_counter()
    logger.info(f"Fine - Elapsed Time: {end - start}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        if PROVA:
            logger.info(e, exc_info=True)
        else:
            logger.critical(e, exc_info=True)

