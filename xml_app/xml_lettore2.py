import os
import xml.etree.ElementTree as ET
from logging import DEBUG

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
ET.parse("smiley.svg")

# Parse XML from a file object
with open("smiley.svg") as file:
    tree = ET.parse(file)

# Parse XML from a Python string
ET.fromstring(
    """\
<svg viewBox="-105 -100 210 270">
  <!-- More content goes here... -->
</svg>
"""
)

root = tree.getroot()
for descendant in root.iter():
    print(descendant.tag)
    print(descendant.text)

tag_name = "{http://www.w3.org/2000/svg}ellipse"
for descendant in root.iter(tag_name):
    print(descendant)
