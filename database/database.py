import settings
import threading
import sqlite3
import os
import utils

logger = utils.get_logger(__file__)
CURRENT_DIRPATH = os.path.dirname(__file__)
TABLES_PATH = os.path.join(CURRENT_DIRPATH, "table.sql")
DATABASE_NAME = "dados.db"
if settings.DEVELOPMENT:
    DATABASE_NAME = "data.db"
    logger.warning("Using {DATABASE_NAME} as current database")
DATABASE_PATH = os.path.join(settings.ROOT_DIRPATH, DATABASE_NAME)


class Database:
    lock = threading.Lock()
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    conn.row_factory = lambda c, r: dict([(col[0], r[idx]) for idx, col in enumerate(c.description)])
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = true;")
    with open(TABLES_PATH) as f:
        cursor.executescript(f.read())

    def __enter__(self):
        logger.debug("Acquiring lock")
        self.lock.acquire()
        logger.debug("Lock acquired")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is None:
            self.conn.commit()
            logger.debug("Commited")
        else:
            self.conn.rollback()
            logger.debug(exc_type)
            logger.debug(exc_val)
            logger.warning("Rolledback")

        logger.debug("Realeasing lock")
        self.lock.release()

    def insert(self, sql: str, **kwargs):
        try:
            logger.debug(F"SQL Insert: {sql}")
            logger.debug(F"Values: {kwargs}")
            self.cursor.execute(sql, kwargs)
            return self.cursor.lastrowid
        except Exception as e:
            logger.exception(e)
            raise

    def select(self, sql: str, **kwargs):
        try:
            logger.debug(F"SQL Select: {sql}")
            logger.debug(F"Values: {kwargs}")
            self.cursor.execute(sql, kwargs)
            return self.cursor.fetchall()
        except Exception as e:
            logger.exception(e)
            raise

    def update(self, sql: str, **kwargs):
        try:
            logger.debug(F"SQL Update: {sql}")
            logger.debug(F"Values: {kwargs}")
            self.cursor.execute(sql, kwargs)
        except Exception as e:
            logger.exception(e)
            raise

    def delete(self, sql: str, **kwargs):
        try:
            logger.debug(F"SQL Delete: {sql}")
            logger.debug(F"Values: {kwargs}")
            self.cursor.execute(sql, kwargs)
        except Exception as e:
            logger.exception(e)
            raise
