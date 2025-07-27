import sys
import os
from servizio import log_setup
import prova
import logging


# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

filename, _ = os.path.splitext(os.path.basename(__file__))
logger = log_setup.logging_setup(
    nomefile=filename, levelfile="DEBUG", name=__name__)

logger.info("Inizio")
def main():
    for item in range(10):
        logger.info(item)

    prova.main()



logger.info("Fine")

if __name__ == "__main__":
    main()