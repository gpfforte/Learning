from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


PROVA = bool(os.environ.get("AMBIENTE_DI_PROVA") == "SI")
# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Setta il log
filename, _ = os.path.splitext(os.path.basename(__file__))

# parametri di accesso al DB su Heroku
DB_POSTGRESQL_NAME = os.environ.get("DB_POSTGRESQL_NAME")
DB_POSTGRESQL_USER = os.environ.get("DB_POSTGRESQL_USER")
DB_POSTGRESQL_PWD = os.environ.get("DB_POSTGRESQL_PWD")
DB_POSTGRESQL_HOST = os.environ.get("DB_POSTGRESQL_HOST")
DB_POSTGRESQL_PORT = os.environ.get("DB_POSTGRESQL_PORT")

db_heroku_uri = f"postgresql://{DB_POSTGRESQL_USER}:{DB_POSTGRESQL_PWD}@{DB_POSTGRESQL_HOST}:{DB_POSTGRESQL_PORT}/{DB_POSTGRESQL_NAME}"

engine = create_engine(db_heroku_uri, echo=False, future=True)
# engine = create_engine('postgresql://usr:pass@localhost:5432/sqlalchemy')
Session = sessionmaker(bind=engine)

Base = declarative_base()
