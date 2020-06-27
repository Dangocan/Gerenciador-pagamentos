import json
import logging
import settings
import os


def get_logger(path: str, log_name: str = None, propagate: bool = False) -> logging.Logger:
    if log_name is None:
        log_name = os.path.splitext(os.path.relpath(path, settings.ROOT_DIRPATH).replace("\\", "_").replace("/", "_"))[0] + ".log"
    logger_maker = logging.getLogger(log_name)
    if os.path.splitext(log_name)[1] != ".log":
        log_name += ".log"
    filepath = os.path.join(settings.LOG_DIRPATH, log_name)
    logger_maker.setLevel(logging.DEBUG)
    fh = logging.FileHandler(filepath, "w" if settings.DEVELOPMENT else "a", encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(settings.LOG_FORMAT))
    logger_maker.addHandler(fh)
    logger_maker.propagate = propagate
    if settings.DEVELOPMENT:
        logger_maker.warning("DEVELOPMENT MODE")
    return logger_maker


def get_keys() -> dict:
    with open(settings.KEYS_PATH, "r", encoding="utf8") as f:
        return json.load(f)


CURRENT_DIRPATH = os.path.dirname(__file__)
logger = get_logger(__file__)
