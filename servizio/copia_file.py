import contextlib
import os
import shutil as sh
from logging import DEBUG
from os.path import isfile, join
from time import perf_counter

from servizio import log_setup

start = perf_counter()
PROVA = bool(os.environ.get("AMBIENTE_DI_PROVA") == "SI")
# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Setta il log
filename, _ = os.path.splitext(os.path.basename(__file__))
logger = log_setup.logging_setup(nomefile=filename, levelfile=DEBUG, name=__name__)

logger.info("Inizio")

src_dir = "C:\\Users\\forteg\\OneDrive - Fratelli Carli Spa\\Desktop\\Python"
dest_dir = "//carlidisk/comune/Forte/python"
# ignore any files but files with '.py' and '.ipynb' extension


def ignore_func(d, files):
    lista = [
        f
        for f in files
        if isfile(join(d, f))
        and f[-3:] != ".py"
        and f[-6:] != ".ipynb"
        and f[-4:] != ".bat"
        and f[-5:] != ".list"
        and f[-4:] != ".cfg"
    ]
    lista.extend(
        (
            "Documentazione",
            ".git",
            ".ipynb_checkpoints",
            "Situazione_Consegne.db",
            ".ssh",
            ".vscode",
            "Training",
            "venvpgadmin",
        )
    )

    return lista


#


def remove_empty_dir(path):
    with contextlib.suppress(OSError):
        os.rmdir(path)


def remove_empty_dirs(path):
    for root, dirnames, filenames in os.walk(path, topdown=False):
        for dirname in dirnames:
            remove_empty_dir(os.path.realpath(os.path.join(root, dirname)))


def main():
    sh.copytree(src_dir, dest_dir, ignore=ignore_func, dirs_exist_ok=True)
    remove_empty_dirs(dest_dir)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        if PROVA:
            logger.info(e, exc_info=True)
        else:
            logger.critical(e, exc_info=True)

end = perf_counter()

logger.info(f"Fine - Elapsed Time: {end - start}")




