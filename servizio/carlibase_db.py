import os
from logging import DEBUG
from time import perf_counter

from sqlalchemy import MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import registry

from servizio import log_setup
from servizio.connessioni import engine_carlibase, session_carlibase

# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Setta il log
filename, _ = os.path.splitext(os.path.basename(__file__))
logger = log_setup.logging_setup(nomefile=filename, levelfile=DEBUG, name=__name__)

PROVA = bool(os.environ.get("AMBIENTE_DI_PROVA") == "SI")
metadata = MetaData()

lista_tabelle_schema_sf = [
    "ORDINI",
    "ORDINI_ITEM",
    "RETSCO",
    "ACCOUNT",
    "CONTACTS",
    "CONSENSI",
]
lista_tabelle_schema_dist = [
    "HUB",
    "TRANSITPOINT",
    "ZONA",
    "TRASPORTATORE",
    "TP_ZONA_TARIFFA",
]
lista_tabelle_schema_sped = ["CONSEGNA", "COLLO"]
lista_tabelle_schema_loc = ["NAZIONE"]
lista_tabelle_schema_fat = ["RESO", "RESO_CONFEZIONE"]

# lista_tabelle_schema_dbo = ["PR_CONFEZ", "PR_CONFARTMGZ"]

# metadata.reflect(
#     # , schema="SQLDATA2012.DataWarehouse.[dbo]"
#     engine_carlibase, only=lista_tabelle_schema_dbo, views=True, schema="SQLDATA2012.DataWarehouse.[dbo]"
#     # engine_carlibase, only=lista_tabelle_schema_dbo, views=True, schema="DataWarehouse.dbo"
# )

metadata.reflect(
    engine_carlibase, only=lista_tabelle_schema_sf, views=True, schema="SF"
)

metadata.reflect(
    engine_carlibase, only=lista_tabelle_schema_dist, views=True, schema="DIST"
)

metadata.reflect(
    engine_carlibase, only=lista_tabelle_schema_sped, views=True, schema="SPED"
)

metadata.reflect(
    engine_carlibase, only=lista_tabelle_schema_loc, views=True, schema="LOC"
)

metadata.reflect(
    engine_carlibase, only=lista_tabelle_schema_fat, views=True, schema="FAT"
)

BaseAuto = automap_base(metadata=metadata)
BaseAuto.prepare()
mapper_registry = registry()

SF_ordini = BaseAuto.classes.ORDINI
SF_ordini_item = BaseAuto.classes.ORDINI_ITEM
SF_account = BaseAuto.classes.ACCOUNT
SF_contacts = BaseAuto.classes.CONTACTS
SF_consensi = BaseAuto.classes.CONSENSI
DIST_hub = BaseAuto.classes.HUB
DIST_transitpoint = BaseAuto.classes.TRANSITPOINT
DIST_zona = BaseAuto.classes.ZONA
DIST_trasportatore = BaseAuto.classes.TRASPORTATORE
DIST_tp_zona_tariffa = BaseAuto.classes.TP_ZONA_TARIFFA
SPED_consegna = BaseAuto.classes.CONSEGNA
SPED_collo = BaseAuto.classes.COLLO
LOC_nazione = BaseAuto.classes.NAZIONE
FAT_reso = BaseAuto.classes.RESO
FAT_reso_confezione = BaseAuto.classes.RESO_CONFEZIONE
# PR_confez = BaseAuto.classes.PR_CONFEZ
# PR_confartmgz = BaseAuto.classes.PR_CONFARTMGZ


def main():
    start = perf_counter()
    with session_carlibase:
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


