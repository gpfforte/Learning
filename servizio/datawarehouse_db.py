import os
from logging import DEBUG
from time import perf_counter

from sqlalchemy import MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import registry

from servizio import log_setup
from servizio.connessioni import engine_datawarehouse, session_datawarehouse

# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Setta il log
filename, _ = os.path.splitext(os.path.basename(__file__))
logger = log_setup.logging_setup(
    nomefile=filename, levelfile=DEBUG, name=__name__)

PROVA = bool(os.environ.get("AMBIENTE_DI_PROVA") == "SI")
metadata = MetaData()

lista_tabelle_schema_dbo = ["PR_CONFEZ", "PR_CONFARTMGZ"]
metadata.reflect(
    engine_datawarehouse, only=lista_tabelle_schema_dbo, views=True, schema="dbo"
)

BaseAuto = automap_base(metadata=metadata)
BaseAuto.prepare()
mapper_registry = registry()

PR_confez = BaseAuto.classes.PR_CONFEZ
PR_confartmgz = BaseAuto.classes.PR_CONFARTMGZ


def main():
    start = perf_counter()
    with session_datawarehouse:
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
