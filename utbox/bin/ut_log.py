import os
import logging, logging.handlers


def setup_logger():
    logger = logging.getLogger('utbox')
    logger.setLevel(logging.DEBUG)

    file_handler = logging.handlers.RotatingFileHandler(
        os.environ['SPLUNK_HOME'] + '/var/log/splunk/utbox.log',
        maxBytes=25000000,
        backupCount=3
        )
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger
