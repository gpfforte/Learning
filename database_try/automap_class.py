from sqlalchemy import inspect
from logging import DEBUG
import datetime as dt
from servizio import log_setup
import os
from time import perf_counter
import os
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy import func

start = perf_counter()
# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Setta il log
filename, _ = os.path.splitext(os.path.basename(__file__))
logger = log_setup.logging_setup(
    nomefile=filename, levelfile="DEBUG", name=__name__)
logger.info("Inizio")

PROVA = bool(os.environ.get("AMBIENTE_DI_PROVA") == "SI")


def main():
    Base = automap_base()

    # engine, suppose it has two tables 'user' and 'address' set up
    engine = create_engine("sqlite:///gestionale.db")
    # print(inspect(engine).get_table_names())
    # print(engine.table_names())
    # reflect the tables

    # Coffee = Base.classes.coffee
    # Orders = Base.classes.orders

    class Orders(Base):
        __tablename__ = "orders"

        def __repr__(self) -> str:
            return f"Order {self.id_order} from {self.customers}"

    class Customers(Base):
        __tablename__ = "customers"

        def __repr__(self) -> str:
            return f"Customer {self.id_customer} {self.first_name} {self.last_name}"

    Base.prepare(engine, reflect=True)
    # print(dir(Orders))
    # for item in Base.classes:
    #     print(item.__table__.columns)
    #     print(dir(item))
    # print(Customers.__table__.columns)
    # print(Orders.__dict__)

    # # Other = Base.classes.other
    session = Session(engine)
    # # # session.add(Coffee(name="GPF", price=100))
    # # session.commit()
    # stmt = select(Coffee).order_by(Coffee.price.desc())

    # print("Count", session.scalar(stmt).count())
    print("Count", session.query(func.count(Orders.id_order)).scalar())
    # results = session.execute(stmt)
    # coffee = session.scalars(stmt).first()
    print(type(inspect(Orders).selectable))
    print("La query seguente 'indovina' la join")
    stmt = select(Orders).join(Customers).where(Customers.last_name == "Elder")
    print(stmt)
    orders = session.scalars(stmt)
    for result in orders:
        print(result)
    print(
        "La query seguente ha una join esplicita attraberso la relazione Orders.customers"
    )
    stmt = select(Orders).join(Orders.customers).where(
        Customers.last_name == "Elder")
    print(stmt)
    orders = session.scalars(stmt)
    for result in orders:
        print(result)

    # print(dir(Coffee))
    # print(Coffee.__repr__)
    # print(Other.columns)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        if PROVA:
            logger.info(e, exc_info=True)
        else:
            logger.critical(e, exc_info=True)
logger.info("Fine")
end = perf_counter()
print("Elapsed Time: ", end - start)
