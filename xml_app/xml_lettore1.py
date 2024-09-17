import os
from logging import DEBUG
from xml.dom.pulldom import parse

from servizio import log_setup

PROVA = bool(os.environ.get("AMBIENTE_DI_PROVA") == "SI")
# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Setta il log
filename, _ = os.path.splitext(os.path.basename(__file__))
logger = log_setup.logging_setup(
    nomefile=filename, levelfile=DEBUG, name=__name__)
event_stream = parse("smiley.svg")
for event, node in event_stream:
    print(event, node)
