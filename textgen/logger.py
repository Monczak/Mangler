import logging
import sys


LOGGER_NAME = "mangler"


def get_logger():
    return logging.getLogger(LOGGER_NAME)


def setup_logger():
    logger = get_logger()
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("[%(asctime)s: %(levelname)s/%(module)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
