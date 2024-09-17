import os
from dataclasses import dataclass
from logging import DEBUG
from time import perf_counter

from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
    create_engine,
    select,
    update,
)
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, declarative_base, relationship
from sqlalchemy.schema import UniqueConstraint

from servizio import log_setup

"""
Questo script prevede di accedere al db su Supabase, quindi
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
logger = log_setup.logging_setup(nomefile=filename, levelfile=DEBUG, name=__name__)
# parametri di accesso al DB su Supabase
DB_POSTGRESQL_NAME = os.environ.get("DB_POSTGRESQL_SUPABASE_NAME")
DB_POSTGRESQL_USER = os.environ.get("DB_POSTGRESQL_SUPABASE_USER")
DB_POSTGRESQL_PWD = os.environ.get("DB_POSTGRESQL_SUPABASE_PWD")
DB_POSTGRESQL_HOST = os.environ.get("DB_POSTGRESQL_SUPABASE_HOST")
DB_POSTGRESQL_PORT = os.environ.get("DB_POSTGRESQL_SUPABASE_PORT")


db_supabase_uri = f"postgresql://{DB_POSTGRESQL_USER}:{DB_POSTGRESQL_PWD}@{DB_POSTGRESQL_HOST}:{DB_POSTGRESQL_PORT}/{DB_POSTGRESQL_NAME}"
# db_supabase_uri = f"postgres://postgres.htqmxzuksolrjhxclwwg:{DB_POSTGRESQL_PWD}@aws-0-eu-central-1.pooler.supabase.com:6543/postgres"
# https://www.postgresql.org/docs/9.0/libpq-ssl.html#LIBPQ-SSL-SSLMODE-STATEMENTS

path_to_crt = os.path.join(
    os.path.expanduser("~"), "AppData", "Roaming", "postgresql", "prod-ca-2021.crt"
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


class Prova(Base):
    __tablename__ = "prova"
    id = Column(Integer, primary_key=True)
    username = Column(String)

    def __repr__(self):
        return f"Prova ({self.username})"


# BaseAuto.prepare(autoload_with=engine, reflect=True, reflection_options={'only': [
#                  "auth_group", "auth_user", "auth_user_groups"]})

# BaseAuto.prepare(autoload_with=engine, reflect=True)
# Base.metadata.create_all(engine)


def update_db():
    with session:
        # stmt = select(Prova).update(username='gpf')
        table = Prova.__table__
        stmt = update(table).values(username="gpf")
        with engine.begin() as conn:
            conn.execute(stmt)
        session.commit()


def select_db():
    with session:
        # stmt = select(Prova).update(username='gpf')
        table = Prova.__table__
        stmt = select(Prova)
        for item in session.scalars(stmt):
            print(item)


def create_db():
    with session:
        Base.metadata.create_all(engine)


def main():
    # create_db()
    # update_db()
    select_db()
    pass


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

