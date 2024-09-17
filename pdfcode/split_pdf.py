import os
from time import perf_counter

from PyPDF2 import PdfMerger, PdfReader, PdfWriter

from servizio import log_setup

start = perf_counter()
# Setta la working directory al path dello script
file_input = "Trattamento_dati_personali.pdf"
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
dname_arch = os.path.join(dname, "archivio")
dname_input = os.path.join(dname, "da_splittare")
path_input = os.path.join(dname_input, file_input)

# Setta il log
filename, _ = os.path.splitext(os.path.basename(__file__))
logger = log_setup.logging_setup(
    nomefile=filename, levelfile="DEBUG", name=__name__)
logger.info("Inizio")

PROVA = bool(os.environ.get("AMBIENTE_DI_PROVA") == "SI")
inputpdf = PdfReader(open(path_input, "rb"))


def main():
    for i in range(len(inputpdf.pages)):
        output = PdfWriter()
        output.add_page(inputpdf.pages[i])
        with open(f"{dname_arch}/{file_input[:-4]}-page{i+1}.pdf", "wb") as outputStream:
            output.write(outputStream)


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
