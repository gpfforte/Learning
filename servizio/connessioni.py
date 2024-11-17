import os
import urllib
from logging import DEBUG

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from servizio import log_setup

# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Setta il log
filename, _ = os.path.splitext(os.path.basename(__file__))
logger = log_setup.logging_setup(nomefile=filename, levelfile=DEBUG, name=__name__)

PROVA = bool(os.environ.get("AMBIENTE_DI_PROVA") == "SI")

conn_string = os.environ.get("CONN_CARLIBASE_TRUSTED")
params = urllib.parse.quote_plus(conn_string)
engine_carlibase = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
session_carlibase = Session(engine_carlibase)

conn_string = os.environ.get("CONN_CARLI_TRUSTED")
params = urllib.parse.quote_plus(conn_string)
engine_carlitraspo = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
session_carlitraspo = Session(engine_carlitraspo)

conn_string = os.environ.get("CONN_DATAWAREHOUSE_TRUSTED")
params = urllib.parse.quote_plus(conn_string)
engine_datawarehouse = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
session_datawarehouse = Session(engine_datawarehouse)

conn_string = os.environ.get("CONN_WMS_TRUSTED")
params = urllib.parse.quote_plus(conn_string)
engine_wms = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
session_wms = Session(engine_wms)

conn_string = os.environ.get("CONN_CARLI")
params = urllib.parse.quote_plus(conn_string)
engine_carli_generic = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
session_carli_generic = Session(engine_carli_generic)
