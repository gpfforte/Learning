import os
from logging import DEBUG
from pathlib import Path
from time import perf_counter

from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

from servizio import log_setup

PROVA = bool(os.environ.get("AMBIENTE_DI_PROVA") == "SI")
BASE_DIR = Path(__file__).resolve().parent

filename, _ = os.path.splitext(os.path.basename(__file__))
logger = log_setup.logging_setup(nomefile=filename, levelfile=DEBUG, name=__name__)

# parametri di accesso al DB su Supabase
DB_POSTGRESQL_NAME = os.environ.get("DB_POSTGRESQL_SUPABASE_NAME")
DB_POSTGRESQL_USER = os.environ.get("DB_POSTGRESQL_SUPABASE_USER")
DB_POSTGRESQL_PWD = os.environ.get("DB_POSTGRESQL_SUPABASE_PWD")
DB_POSTGRESQL_HOST = os.environ.get("DB_POSTGRESQL_SUPABASE_HOST")
DB_POSTGRESQL_PORT = os.environ.get("DB_POSTGRESQL_SUPABASE_PORT")

db_supabase_uri = f"postgresql://{DB_POSTGRESQL_USER}:{DB_POSTGRESQL_PWD}@{DB_POSTGRESQL_HOST}:{DB_POSTGRESQL_PORT}/{DB_POSTGRESQL_NAME}"
# https://www.postgresql.org/docs/9.0/libpq-ssl.html#LIBPQ-SSL-SSLMODE-STATEMENTS

path_to_crt = os.path.join(BASE_DIR, "prod-ca-2021.crt")

engine_sb = create_engine(
    db_supabase_uri,
    connect_args={
        "sslmode": "verify-full",
        "sslrootcert": path_to_crt,
    },
    echo=False,
    future=True,
)

session_sb = Session(engine_sb)


def main():
    start = perf_counter()
    metadata = MetaData()
    metadata.reflect(
        engine_sb,
    )
    BaseAuto = automap_base(metadata=metadata)
    BaseAuto.prepare()
    with session_sb:
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
        # print(DB_POSTGRESQL_PORT)
    except Exception as e:
        if PROVA:
            logger.info(e, exc_info=True)
        else:
            logger.critical(e, exc_info=True)

