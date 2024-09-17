from sqlalchemy import create_engine, ForeignKey, select
from sqlalchemy.orm import Session
from sqlalchemy import Column, Date, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
import os
from logging import DEBUG
from servizio import log_setup
import os
from time import perf_counter

start = perf_counter()

PROVA = bool(os.environ.get("AMBIENTE_DI_PROVA") == "SI")
# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Setta il log
filename, _ = os.path.splitext(os.path.basename(__file__))
logger = log_setup.logging_setup(
    nomefile=filename, levelfile=DEBUG, name=__name__)

logger.info("Inizio")

engine = create_engine("sqlite:///coffee.db", echo=True, future=True)
Base = declarative_base()


class Coffee(Base):
    __tablename__ = "coffee"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)

    def __repr__(self):
        return f"id = {self.id}, name = {self.name}, price = {self.price}"


# Base.metadata.create_all(engine)
def inserisci():
    with Session(engine) as session:
        coffe1 = Coffee(
            name="Churrasco",
            price=21,
        )
        session.add_all([coffe1])
        session.commit()


def seleziona():
    session = Session(engine)
    coffees = select(Coffee).where(Coffee.name.in_(["caffeina", "Kimbo"]))
    # coffees = select(Coffee)
    print(type(coffees))
    # print(coffees)
    for coffee in session.scalars(coffees):
        print(coffee)


def main():
    # La parte sotto serve solo all'inizio per creare la tabella altrimenti non fa nulla
    # Base.metadata.create_all(engine)
    seleziona()


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
