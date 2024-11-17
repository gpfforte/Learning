import datetime as dt
import os
import pathlib
from time import perf_counter

from servizio import log_setup

PROVA = bool(os.environ.get("AMBIENTE_DI_PROVA") == "SI")
start = perf_counter()

# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

filename, _ = os.path.splitext(os.path.basename(__file__))
logger = log_setup.logging_setup(
    nomefile=filename, levelfile="DEBUG", name=__name__)

# Lista path da pulire
lista_path = [
    "//carlidisk/comune/Forte",
    "//carlidisk/trasporti/BRT",
    "C:/Users/forteg/OneDrive - Fratelli Carli Spa/Desktop/Python/EsitiBRT/archivio",
    "C:/Users/forteg/OneDrive - Fratelli Carli Spa/Desktop/Python/ordini_hotel",
    "C:/Users/forteg/OneDrive - Fratelli Carli Spa/Desktop/Python/Resi",
    "C:/Users/forteg/OneDrive - Fratelli Carli Spa/Desktop/Python/Situazione_Consegne/archivio",
    "C:/Users/forteg/OneDrive - Fratelli Carli Spa/Desktop/Python/ordini_hotel/archivio",
    "C:/Users/forteg/OneDrive - Fratelli Carli Spa/Desktop/Python/Resi/archivio",
    "C:/Users/forteg/OneDrive - Fratelli Carli Spa/Desktop/Python/kpi/archivio",
    "C:/Users/forteg/Desktop/Python/EsitiBRT/archivio",
    "C:/Users/forteg/Desktop/Python/ordini_hotel",
    "C:/Users/forteg/Desktop/Python/Resi",
    "C:/Users/forteg/Desktop/Python/Situazione_Consegne/archivio",
    "C:/Users/forteg/Desktop/Python/ordini_hotel/archivio",
    "C:/Users/forteg/Desktop/Python/Resi/archivio",
    "C:/Users/forteg/Desktop/Python/kpi/archivio",
]

today = dt.datetime.now()
startdate = today + dt.timedelta(days=-15)

logger.info(f"Cancella file più vecchi di {startdate}")
conteggio = 0


def main():
    global conteggio
    for path in lista_path:
        try:
            os.chdir(path)
        except:
            continue
        files = os.listdir(path)
        # logger.info(files)
        # for file in files:
        #     print(file[-3:].lower())

        files_csv = [f for f in files if f[-3:].lower() == "csv"]
        # logger.info(path)
        # logger.info(files_csv)
        # Cancello i file più vecchi di x giorni
        for f in files_csv:
            fname = pathlib.Path(f)
            ctime = dt.datetime.fromtimestamp(fname.stat().st_ctime)
            mtime = dt.datetime.fromtimestamp(fname.stat().st_mtime)
            compare_time = max(ctime, mtime)
            logger.info(f"ctime {ctime} del file  {path}/{f}")
            if compare_time < startdate:
                # print(path, f)
                conteggio += 1
                logger.info(f"File cancellato: {path}/{f}")
                os.remove(fname)


logger.info("Inizio")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        if PROVA:
            logger.info(e, exc_info=True)
        else:
            logger.critical(e, exc_info=True)
logger.info(f"Numero File Cancellati: {conteggio}")
logger.info("Fine")
end = perf_counter()
logger.info(f"Elapsed Time: {end - start}")
