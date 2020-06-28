import os
import platform

DEVELOPMENT = platform.system() == "Windows"
ROOT_DIRPATH = os.path.dirname(__file__)
LOG_DIRPATH = os.path.join(ROOT_DIRPATH, "log")
TEMPLATES_FOLDER = os.path.join(ROOT_DIRPATH, "templates")
STATIC_FOLDER = os.path.join(ROOT_DIRPATH, "static")

KEYS_PATH = os.path.join(ROOT_DIRPATH, "keys.json")
STDDATETIMEFORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
LOG_FORMAT = "%(asctime)s - %(levelname)s :: %(name)s %(lineno)d :: %(message)s"

os.makedirs(LOG_DIRPATH, exist_ok=True)
