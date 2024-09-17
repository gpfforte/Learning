import os
from time import perf_counter

from PyPDF2 import PdfMerger

from servizio import log_setup

start = perf_counter()
# Setta la working directory al path dello script
file_dest = "Result.pdf"
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
dname_arch = os.path.join(dname, "archivio")
dname_aggr = os.path.join(dname, "da_aggregare")
path_dest = os.path.join(dname_arch, file_dest)
# print('abspath', abspath)
# print('dname', dname)
# print('dname_arch', dname_arch)
# print('path_dest', path_dest)
# print('os.path.exists(path_dest)', os.path.exists(path_dest))

# Setta il log
filename, _ = os.path.splitext(os.path.basename(__file__))
logger = log_setup.logging_setup(
    nomefile=filename, levelfile="DEBUG", name=__name__)
logger.info("Inizio")

PROVA = bool(os.environ.get("AMBIENTE_DI_PROVA") == "SI")


def main():
    if not os.path.exists(path_dest):
        files = os.listdir(dname_aggr)
        pdfs = [f for f in files if f[-3:] == "pdf"]
        if pdfs:
            pdfs.sort()
            merger = PdfMerger(strict=False)

            for pdf in pdfs:
                merger.append(open(os.path.join(dname_aggr, pdf), "rb"))

            merger.write(path_dest)
            merger.close()
            print("Attività Completata")
        else:
            print("Non ci sono file da aggregare")
    else:
        print("Esiste già il file destinazione, impossibile procedere")


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
logger.info(f"Elapsed Time: {end - start}")
