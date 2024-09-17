import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'servizio'))
import log_setup


# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
#  Impostazione logging, come parametro passo il nome del file di log
filename, _ = os.path.splitext(os.path.basename(__file__))
logger = log_setup.logging_setup(nomefile=filename, levelfile="DEBUG", name=__name__)
#  Impostazione logging, come parametro passo il nome del file di log
# logger = log_setup.logging_setup(nomefile="prova", levelfile="DEBUG", name=__name__)
msg="Ciao"
logger.info(msg)

def main():
    logger.info("Main in Prova")
    pass

if __name__=="__main__":
    main()
