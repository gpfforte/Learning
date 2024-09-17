import os

from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Float,
    DateTime,
    func,
    select,
    and_,
)
from sqlalchemy.orm import Session
import urllib
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import declarative_base
from servizio import log_setup
from logging import DEBUG
from time import perf_counter
from sqlalchemy.orm import registry

# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Setta il log
filename, _ = os.path.splitext(os.path.basename(__file__))
logger = log_setup.logging_setup(
    nomefile=filename, levelfile=DEBUG, name=__name__)

conn_string = os.environ.get("CONN_CARLI_TRUSTED")
params = urllib.parse.quote_plus(conn_string)

# print(params)

engine_carlitraspo = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)

session_carlitraspo = Session(engine_carlitraspo)
PROVA = bool(os.environ.get("AMBIENTE_DI_PROVA") == "SI")
metadata = MetaData()
"""
TARIFFE_ZONE_DEP_REPORT è una view e per poterla mappare è stato necessario costruire una Table per definire la primary key, altrimenti non la rilevava.
Successivamente, per poter deinire uno str method ho dovuto definire una class Tariffe da non far ereditare da base ne da autobase e fare un map_imperatively
tra la classe definita e la Table. In questo modo l'oggetto Tariffe è possibile trattarlo come se rappresentasse la definizione di una base o di una autobase
"""
lista_tabelle = [
    "SP_SPED",
    "SP_SPED1",
    "SP_DEPOSITI",
    "SP_TRASPO",
    "SP_ARTMGZ",
    "SP_ESITI",
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
# Tariffe = BaseAuto.classes.TARIFFE_ZONE_DEP_REPORT
Sp_Sped = BaseAuto.classes.SP_SPED
Sp_Sped1 = BaseAuto.classes.SP_SPED1

# BaseAuto.prepare(autoload_with=engine_carlitraspo, reflect=True,
#                  reflection_options={'only': lista_tabelle}, views=True)
# BaseAuto.prepare(autoload_with=engine, reflect=True)


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
    tariffe_data = (
        session_carlitraspo.query(tariffe).where(
            tariffe.c.cod_deposito == "31").all()
    )
    for tariffa in tariffe_data[:5]:
        print(tariffa.cod_deposito)
    subq = (
        session_carlitraspo.query(
            Tariffe.cod_deposito,
            func.max(Tariffe.data_fine_valid).label("max_data_fine_valid"),
        )
        .group_by(Tariffe.cod_deposito)
        .subquery("subq")
    )

    tariffe_data = (
        session_carlitraspo.query(Tariffe)
        .where(
            and_(
                Tariffe.data_fine_valid == subq.c.max_data_fine_valid,
                Tariffe.cod_deposito == subq.c.cod_deposito,
            )
        )
        .order_by(Tariffe.cod_deposito, Tariffe.zona)
    )
    tariffe_data = tariffe_data.where(Tariffe.cod_deposito == "31")
    tariffe_data = tariffe_data.all()
    for tariffa_data in tariffe_data:
        print(tariffa_data.cod_deposito, tariffa_data.zona, tariffa_data.TARIFFA)
        print(tariffa_data)
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
