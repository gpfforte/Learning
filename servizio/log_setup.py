import logging
import os
from logging.handlers import RotatingFileHandler

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

file_name, _ = os.path.splitext(os.path.basename(__file__))

def logging_setup(nomefile="DEBUG", levelfile=logging.DEBUG, name=__name__):
    log_file_format = "%(filename)-20s | [%(levelname)-8s] | %(asctime)s | %(name)-10s | in %(module)-20s : %(lineno)-4d : %(message)s"
    log_console_format = "%(filename)-20s | [%(levelname)-8s] | %(asctime)s | %(name)-10s |in %(module)-20s : %(lineno)-4d : %(message)s"
    log_email_format = '''
        Message type:       %(levelname)s
        Location:           %(pathname)s:%(lineno)d
        Module:             %(module)s
        Function:           %(funcName)s
        Time:               %(asctime)s
        Logger name:        %(name)s

        Message:

        %(message)s
        '''
    root_logger = logging.getLogger()

    main_logger = logging.getLogger(name)
    main_logger.setLevel(logging.DEBUG)
    main_logger.propagate = False
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(log_console_format))

    exp_file_handler = RotatingFileHandler(
        nomefile+".log", maxBytes=10**6, backupCount=5)
    if levelfile == logging.DEBUG:
        exp_file_handler.setLevel(logging.DEBUG)
    if levelfile == logging.INFO:
        exp_file_handler.setLevel(logging.INFO)
    exp_file_handler.setFormatter(logging.Formatter(log_file_format))

    EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
    EMAIL_HOST_SERVER = os.environ.get("EMAIL_HOST_SERVER")
    EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
    mail_handler = logging.handlers.SMTPHandler(mailhost=EMAIL_HOST_SERVER,
                                                fromaddr=EMAIL_HOST_USER,
                                                toaddrs=[
                                                    "gpf_forte@hotmail.com"],
                                                subject='Log Mail for '+nomefile,
                                                credentials=(
                                                    EMAIL_HOST_USER, EMAIL_HOST_PASSWORD),
                                                secure=())
    # Only email errors, not warnings
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(logging.Formatter(log_email_format))

    main_logger.addHandler(console_handler)
    main_logger.addHandler(exp_file_handler)
    main_logger.addHandler(mail_handler)


    main_logger.debug(f"Root Handlers: {root_logger.handlers}")
    main_logger.debug(f"Log Setup Completed, called from {nomefile}")
    main_logger.debug(f"main_logger: {main_logger}")
    main_logger.debug(f"Handlers:{main_logger.handlers}")
    main_logger.info("Log Setup Completed, called from "+nomefile)

    # Ottieni tutti i logger registrati
    all_loggers = logging.Logger.manager.loggerDict

    # Stampa i nomi dei logger
    for logger_name in all_loggers:
        main_logger.debug(f"logger_name: {logger_name}")
        loggatore = logging.getLogger(logger_name)

        main_logger.debug(f"Handlers for {logger_name}: {loggatore.handlers}")

        pass

    return main_logger

def main():
    logger = logging_setup(nomefile=file_name, levelfile=logging.DEBUG, name=__name__)
    logger.info("Log setup main function executed")
    

if __name__=="__main__":
    main()