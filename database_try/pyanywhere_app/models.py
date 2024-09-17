import os
from logging import DEBUG

from sqlalchemy import Column, ForeignKey, Integer, String, create_engine, select
from sqlalchemy.orm import Session, declarative_base, relationship

from servizio import log_setup

Base = declarative_base()
PROVA = bool(os.environ.get("AMBIENTE_DI_PROVA") == "SI")
# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Setta il log
filename, _ = os.path.splitext(os.path.basename(__file__))
logger = log_setup.logging_setup(
    nomefile=filename, levelfile=DEBUG, name=__name__)

# engine = create_engine('sqlite:///underwater.db', echo=False, future=True)

PY_ANYWHERE_MYSQL_DB_NAME = os.environ.get("PY_ANYWHERE_MYSQL_DB_NAME")
PY_ANYWHERE_MYSQL_USER = os.environ.get("PY_ANYWHERE_MYSQL_USER")
PY_ANYWHERE_MYSQL_PWD = os.environ.get("PY_ANYWHERE_MYSQL_PWD")
PY_ANYWHERE_MYSQL_USER_HOST = os.environ.get("PY_ANYWHERE_MYSQL_USER_HOST")
# DB_POSTGRESQL_PORT = os.environ.get("DB_POSTGRESQL_PORT")
################ ONLY WITH PAID ACCOUNT YOU CAN ACCESS FROM OUTSIDE ####################
################ ONLY WITH PAID ACCOUNT YOU CAN ACCESS FROM OUTSIDE ####################
################ ONLY WITH PAID ACCOUNT YOU CAN ACCESS FROM OUTSIDE ####################
################ ONLY WITH PAID ACCOUNT YOU CAN ACCESS FROM OUTSIDE ####################
################ ONLY WITH PAID ACCOUNT YOU CAN ACCESS FROM OUTSIDE ####################
################ ONLY WITH PAID ACCOUNT YOU CAN ACCESS FROM OUTSIDE ####################
################ ONLY WITH PAID ACCOUNT YOU CAN ACCESS FROM OUTSIDE ####################

db_pyanywhere_uri = f"mysql+mysqldb://{PY_ANYWHERE_MYSQL_USER}:{PY_ANYWHERE_MYSQL_PWD}@{PY_ANYWHERE_MYSQL_USER_HOST}/{PY_ANYWHERE_MYSQL_DB_NAME}"
engine = create_engine(db_pyanywhere_uri, echo=False, future=True)


class User(Base):
    __tablename__ = "user_account"
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    fullname = Column(String)
    nickname = Column(String)
    addresses = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)
    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


def main():
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(e, exc_info=True)
