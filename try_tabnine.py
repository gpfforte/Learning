# import pandas as pd
# import numpy as np
from logging import DEBUG
from servizio import log_setup
import os
from time import perf_counter

start = perf_counter()

# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Setta il log
filename, _ = os.path.splitext(os.path.basename(__file__))
logger = log_setup.logging_setup(
    nomefile=filename, levelfile=DEBUG, name=__name__)

logger.info("Inizio")

PROVA = bool(os.environ.get("AMBIENTE_DI_PROVA") == "SI")

filename = "try_tabnine.txt"


def main():
    try:
        with open(filename, "r") as f:
            # row = True
            # while row:
            #     row = f.readline()
            #     print(row)
            for line in f:
                print(line.rstrip("\n"))
    except Exception as e:
        if PROVA:
            logger.info(e, exc_info=True)
        else:
            logger.critical(e, exc_info=True)
    # Altro codice


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
