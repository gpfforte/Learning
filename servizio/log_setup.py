import logging
import os
from logging import DEBUG, INFO
from logging.handlers import RotatingFileHandler


def logging_setup(nomefile="DEBUG", levelfile=DEBUG, name=__name__):
    log_file_format = "%(filename)s | [%(levelname)s] | %(asctime)s | %(name)s | : %(message)s in %(module)s:%(lineno)d"
    log_console_format = "[%(levelname)s] | : %(message)s in %(module)s:%(lineno)d"
    log_email_format = '''
        Message type:       %(levelname)s
        Location:           %(pathname)s:%(lineno)d
        Module:             %(module)s
        Function:           %(funcName)s
        Time:               %(asctime)s

        Message:

        %(message)s
        '''

    main_logger = logging.getLogger(name)
    main_logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(log_console_format))

    exp_file_handler = RotatingFileHandler(
        nomefile+".log", maxBytes=10**6, backupCount=5)
    if levelfile == DEBUG:
        exp_file_handler.setLevel(logging.DEBUG)
    if levelfile == INFO:
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

    main_logger.info("Log Setup Completed, called from "+nomefile)

    return main_logger
