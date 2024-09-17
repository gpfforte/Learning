from dataclasses import dataclass
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import select
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy.schema import UniqueConstraint
from logging import DEBUG
from servizio import log_setup
import os
from time import perf_counter

"""
Questo script prevede di accedere al db su Supabase quindi
nelle credenziali devono esserci quelle
"""

start = perf_counter()

Base = declarative_base()
BaseAuto = automap_base()
PROVA = bool(os.environ.get("AMBIENTE_DI_PROVA") == "SI")
# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Setta il log
filename, _ = os.path.splitext(os.path.basename(__file__))
logger = log_setup.logging_setup(
    nomefile=filename, levelfile=DEBUG, name=__name__)
# parametri di accesso al DB su Supabase
DB_POSTGRESQL_NAME = os.environ.get("DB_POSTGRESQL_NAME")
DB_POSTGRESQL_USER = os.environ.get("DB_POSTGRESQL_USER")
DB_POSTGRESQL_PWD = os.environ.get("DB_POSTGRESQL_PWD")
DB_POSTGRESQL_HOST = os.environ.get("DB_POSTGRESQL_HOST")
DB_POSTGRESQL_PORT = os.environ.get("DB_POSTGRESQL_PORT")

db_supabase_uri = f"postgresql://{DB_POSTGRESQL_USER}:{DB_POSTGRESQL_PWD}@{DB_POSTGRESQL_HOST}:{DB_POSTGRESQL_PORT}/{DB_POSTGRESQL_NAME}"
# https://www.postgresql.org/docs/9.0/libpq-ssl.html#LIBPQ-SSL-SSLMODE-STATEMENTS

path_to_crt = os.path.join(
    os.path.expanduser(
        "~"), "AppData", "Roaming", "postgresql", "prod-ca-2021.crt"
)
engine = create_engine(
    db_supabase_uri,
    connect_args={
        "sslmode": "verify-full",
        "sslrootcert": path_to_crt,
    },
    echo=False,
    future=True,
)

session = Session(engine)


class Country(BaseAuto):
    __tablename__ = "countries"

    def __repr__(self):
        return f"Country({self.name}, {self.iso2}, {self.iso3}, {self.local_name}, {self.continent})"

    def __str__(self):
        return f"{self.name} - {self.iso2}"


BaseAuto.prepare(autoload_with=engine, reflect=True)

# BaseAuto.prepare(autoload_with=engine, reflect=True, reflection_options={'only': [
#                  "countries"]})


# Countries = BaseAuto.classes.countries

# print(Countries.__table__.columns.keys())


def main():
    with session:
        # Stampo i nomi di tutte le colonne delle classi/tabelle individuate dal reflect
        for item in BaseAuto.classes:
            print()
            print(item.__table__.name)
            print(item.__table__.columns.keys())
        print()
        countries = session.scalars(
            select(Country).where(Country.continent == "Europe")
        )

        for item in countries:
            print(item, repr(item))
            print([getattr(item, key)
                  for key in Country.__table__.columns.keys()])


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
