import logging
import os
from logging.config import fileConfig


def get_logging(name):
    file_path = os.path.join(os.path.dirname(__file__), 'logging.ini')
    fileConfig(file_path)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    return logger
