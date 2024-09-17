import contextlib
import os
import shutil as sh
from logging import DEBUG
from os.path import isfile, join
from time import perf_counter

from servizio import log_setup

start = perf_counter()
PROVA = bool(os.environ.get("AMBIENTE_DI_PROVA") == "SI")
# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Setta il log
filename, _ = os.path.splitext(os.path.basename(__file__))
logger = log_setup.logging_setup(nomefile=filename, levelfile=DEBUG, name=__name__)

logger.info("Inizio")
contenuto_corrente = os.listdir(os.path.curdir)
for item in contenuto_corrente:
    print(item)
# print(contenuto_corrente)
print(os.path.basename(__file__))
print(os.path.splitext(os.path.basename(__file__)))

