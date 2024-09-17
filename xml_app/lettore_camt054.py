import os
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime as dt
from datetime import timedelta
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


@dataclass
class Transaction:
    valuta: str = ""
    reference_type: str = ""
    reference_value: str = ""
    cod_cliente: str = ""
    num_fattura: int = 0
    data_fattura: str = ""
    importo: float = 0.0

    def __post_init__(self):
        self.cod_cliente = reference_value[-8:-1]
        self.num_fattura = reference_value[-15:-8]
        anno = int(f"20{reference_value[7:12][:2]}")
        giorno_anno = int(reference_value[7:12][2:])
        inizio_anno = dt(year=anno, month=1, day=1).date()
        data_calcolata = inizio_anno + timedelta(days=giorno_anno - 1)
        self.data_fattura = dt.strftime(data_calcolata, "%Y%m%d")

    def __str__(self):
        return f"{self.cod_cliente};{self.data_fattura};{self.num_fattura};{self.importo:010.2f}"


# Parse XML from a file object
with open("CAMT054.xml") as file:
    tree = ET.parse(file)


root = tree.getroot()

# for descendant in root.iter():
#     print(descendant.tag)
#     print(descendant.text)

transaction_list = []

tag_name_prefix = "{urn:iso:std:iso:20022:tech:xsd:camt.054.001.04}"
for descendant in root.iter(f"{tag_name_prefix}TxDtls"):
    valuta = ""
    importo = ""
    reference_type = ""
    reference_value = ""
    # print(descendant.Amt.text)
    for child in descendant:
        # print(child.tag)
        if child.tag == f"{tag_name_prefix}Amt":
            # print(child.attrib["Ccy"], child.text)
            valuta = child.attrib["Ccy"]
            importo = child.text
        if child.tag == f"{tag_name_prefix}RmtInf":
            for item in child:
                if item.tag == f"{tag_name_prefix}Strd":
                    # print(item[0][0][0][0].text)
                    reference_type = item[0][0][0][0].text
                    # print(item[0][1].text)
                    reference_value = item[0][1].text
                    # print(child.attrib["Ccy"], child.text,
                    #       item[0][0][0][0].text, item[0][1].text)
            if reference_type in ("ESR", "QRR"):
                transaction = Transaction(
                    valuta=valuta,
                    importo=float(importo),
                    reference_type=reference_type,
                    reference_value=reference_value,
                )
                transaction_list.append(transaction)

print(len(transaction_list))
for transaction in transaction_list:
    print(repr(transaction))

with open("transaction.txt", "w") as f:
    for transaction in transaction_list:
        f.write(f"{str(transaction)}\n")

# stringa = "004400122237402802052664128"
# print(len(stringa))
