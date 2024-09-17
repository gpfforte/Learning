import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'servizio'))
import log_setup
import prova

# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

filename, _ = os.path.splitext(os.path.basename(__file__))
logger = log_setup.logging_setup(
    nomefile=filename, levelfile="DEBUG", name=__name__)

logger.info("Inizio")

for item in range(10):
    logger.debug(item)

prova.main()

logger.info("Fine")
