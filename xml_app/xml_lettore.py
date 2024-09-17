import os
from logging import DEBUG
from xml.dom.minidom import parse, parseString

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


# Parse XML from a filename
document = parse("smiley.svg")

# Parse XML from a file object
# with open("smiley.svg") as file:
#     document = parse(file)


# # Parse XML from a Python string
# document = parseString("""\
# <svg viewBox="-105 -100 210 270">
#   <!-- More content goes here... -->
# </svg>
# """)

# XML Declaration
print(document.version, document.encoding, document.standalone)


# Document Type Definition (DTD)
dtd = document.doctype
print(dtd.entities["custom_entity"].childNodes)


# Document Root
print(document.documentElement)
