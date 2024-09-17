from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy import select
from logging import DEBUG
from servizio import log_setup
import os
from time import perf_counter
from models import User, Address, engine

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


def inserimento():
    with Session(engine) as session:
        # spongebob = User(
        #     name="spongebob",
        #     fullname="Spongebob Squarepants",
        #     addresses=[Address(email_address="spongebob@sqlalchemy.org")],
        # )
        # sandy = User(
        #     name="sandy",
        #     fullname="Sandy Cheeks",
        #     addresses=[
        #         Address(email_address="sandy@sqlalchemy.org"),
        #         Address(email_address="sandy@squirrelpower.org"),
        #     ],
        # )
        # patrick = User(name="patrick", fullname="Patrick Star")

        # session.add_all([spongebob, sandy, patrick])

        pippucchio = User(
            name="sandy",
            fullname="Sandy Cheeks",
            addresses=[
                Address(email_address="pippo@sqlalchemy.org"),
                Address(email_address="pippo@squirrelpower.org"),
            ],
        )
        session.add(pippucchio)
        session.commit()


def selezione():
    session = Session(engine)
    stmt = select(User).where(User.name.in_(["spongebob", "sandy"]))
    for user in session.scalars(stmt):
        print(user)

    stmt = (
        select(Address)
        .join(Address.user)
        .where(User.name == "sandy")
        # .where(Address.email_address == "sandy@sqlalchemy.org")
    )
    sandy_address = session.scalars(stmt)
    for address in sandy_address:
        print(address)

    stmt = (
        select(Address)
        .join(Address.user)
        .where(User.name == "sandy")
        .where(Address.email_address == "sandy@sqlalchemy.org")
    )
    sandy_address = session.scalars(stmt).one()
    print(sandy_address)


def aggiornamento():
    with Session(engine) as session:
        # stmt = select(User).where(User.id.__eq__(1))
        # spongebob = session.scalars(stmt).one()
        # print(spongebob)
        # spongebob.fullname = "SpongeBob Squarepant"
        # logger.info(session.dirty)

        pippucchio = session.get(User, 5)
        pippucchio.name = "Pippucchio"
        pippucchio.fullname = "Pippucchio Underwater"
        session.commit()


def cancellazione():
    with Session(engine) as session:
        # stmt = select(User).where(User.id.__eq__(1))
        # spongebob = session.scalars(stmt).one()
        # print(spongebob)
        # spongebob.fullname = "SpongeBob Squarepant"
        # logger.info(session.dirty)

        pippucchio = session.get(User, 5)
        session.delete(pippucchio)
        session.commit()


def main():
    # La parte sotto serve solo all'inizio per creare la tabella altrimenti non fa nulla
    # Base.metadata.create_all(engine)
    # inserimento()
    # selezione()
    # aggiornamento()
    cancellazione()


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
