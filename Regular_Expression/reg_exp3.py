import re
from collections import Counter
import pandas as pd
import os
from servizio import log_setup

# print (sys.path)
# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
# Setta il log
filename, _ = os.path.splitext(os.path.basename(__file__))
logger = log_setup.logging_setup(
    nomefile=filename, levelfile="DEBUG", name=__name__)
logger.info("Inizio")
counting = Counter([])


def stampa_match(result):
    global counting
    counting = counting + Counter(result)
    for item in result:
        pass
        # print(item)
    # print("--------------")
    # print(counting)
    # print("--------------")

    # for item in result:
    #     print('Result found: ', "'"+item.group()+"'",
    #           item.start(), item.end(), item.span())


def main():

    # Stringa dentro cui cercare le occorrenze
    test_strings = ["""
    Viva le 120 cose migliori del mondo.
    Viva le 120 cose migliori del mondo.
    pinco.pallino@olio.it
    pallo@olio.edu
    gpf_forte@hotmail.com
    https://www.google.com
    http://coreyms.com
    https://youtube.com
    https://www.nasa.gov
    """, "Pippo pippo pippo pippo pippo pippo pippo pippo pippo"]

    # Regular Expression per cercare match
    re_pattern = re.compile(r"[a-z,A-Z]+")

    print("findall")
    for item in test_strings:
        result = re_pattern.findall(item)
        stampa_match(result)
    print()
    print(counting)
    print("---------------------------")
    print(counting.most_common())
    print("---------------------------")
    print(dict(counting.most_common()))

    # finditer ritorna un iterable di classe match per ogni risultato trovato nella stringa
    # print("finditer")
    # result = re_pattern.finditer(test_string)
    # stampa_match(result)
    # print()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(e, exc_info=True)

logger.info("Fine")
