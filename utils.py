import json
import logging
import settings
import typing
import os


def get_logger(path: str, LOG_NAME: str = None, propagate: bool = False) -> logging.Logger:
    if LOG_NAME is None:
        LOG_NAME = os.path.splitext(os.path.relpath(path, settings.ROOT_DIRPATH).replace("\\", "_").replace("/", "_"))[0] + ".log"
    logger_maker = logging.getLogger(LOG_NAME)
    if os.path.splitext(LOG_NAME)[1] != ".log":
        LOG_NAME += ".log"
    filepath = os.path.join(settings.LOG_DIRPATH, LOG_NAME)
    logger_maker.setLevel(logging.DEBUG)
    fh = logging.FileHandler(filepath, "w" if settings.DEVELOPMENT else "a", encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(settings.LOG_FORMAT))
    logger_maker.addHandler(fh)
    logger_maker.propagate = propagate
    return logger_maker


def get_keys() -> dict:
    with open(settings.KEYS_PATH, "r", encoding="utf8") as f:
        return json.load(f)


CURRENT_DIRPATH = os.path.dirname(__file__)
logger = get_logger(__file__)
