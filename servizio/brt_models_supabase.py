"""
Definizione modelli per riferimenti BRT su Supabase
"""
import datetime as dt
import os
from logging import DEBUG

from sqlalchemy import Column, Date, String
from sqlalchemy.orm import declarative_base

from servizio import log_setup
from servizio.supabase_db import engine_sb

PROVA = bool(os.environ.get("AMBIENTE_DI_PROVA") == "SI")
# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Setta il log
filename, _ = os.path.splitext(os.path.basename(__file__))
logger = log_setup.logging_setup(
    nomefile=filename, levelfile=DEBUG, name=__name__)


Base = declarative_base()


class MapRifCarliBrt(Base):
    """Classe per mappare il riferimento numerico Carli con BRT Code"""
    __tablename__ = "conv_rif_carli_rif_brt"
    riferimento_carli = Column(String, primary_key=True)
    riferimento_brt = Column(String)
    created_at = Column(Date, default=dt.datetime.now)

    def __str__(self):
        return f"Riferimento Carli: {self.riferimento_carli} - Riferimento BRT: {self.riferimento_brt}"


def main():
    """Main"""
    Base.metadata.create_all(engine_sb)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(e, exc_info=True)
