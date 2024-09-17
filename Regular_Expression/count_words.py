import os
import re
from collections import Counter

import pandas as pd

from servizio import log_setup

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


def main():
    global counting
    # Il file seguente è quello in cui si vogliono contare le occorrenze delle parole
    df = pd.read_csv("reg_exp_sample.csv", sep=";")

    # Regular Expression per cercare match
    re_pattern = re.compile(r"[a-z,A-Z]+")
    # re_pattern = re.compile(r"\w+")

    # Di seguito accedo a tutte le righe della prima colonna, gli oggetti Counter sommano i valori a parità
    # di chiave
    for item in df.iloc[:, 0]:
        result = re_pattern.findall(item)
        counting = counting + Counter(result)

    counted_words = dict(counting.most_common())
    df_result = pd.DataFrame(counted_words.items(),
                             columns=['Word', 'Occurences'])
    df_result.to_csv("reg_exp_sample_result.csv",
                     sep=";", index=False)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(e, exc_info=True)

logger.info("Fine")
