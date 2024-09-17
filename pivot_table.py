from logging import DEBUG
from datetime import datetime, timedelta
from servizio import log_setup
import pandas as pd
import os
from time import perf_counter
import os

start = perf_counter()
# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Setta il log
filename, _ = os.path.splitext(os.path.basename(__file__))
logger = log_setup.logging_setup(
    nomefile=filename, levelfile="DEBUG", name=__name__)
logger.info("Inizio")

PROVA = bool(os.environ.get("AMBIENTE_DI_PROVA") == "SI")


def main():
    df = pd.DataFrame(
        {
            "A": ["foo", "foo", "foo", "foo", "foo", "bar", "bar", "bar", "bar"],
            "B": ["one", "one", "one", "two", "two", "one", "one", "two", "two"],
            "C": [
                "small",
                "large",
                "large",
                "small",
                "small",
                "large",
                "small",
                "small",
                "large",
            ],
            "D": [1, 2, 2, 3, 3, 4, 5, 6, 7],
            "E": [2, 4, 5, 5, 6, 6, 8, 9, 9],
        }
    )

    table = pd.pivot_table(df, values=["D", "E"], index=["A"], columns=["C"])
    print(df)
    print(table)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        if PROVA:
            logger.info(e, exc_info=True)
        else:
            logger.critical(e, exc_info=True)
logger.info("Fine")
end = perf_counter()
print("Elapsed Time: ", end - start)
