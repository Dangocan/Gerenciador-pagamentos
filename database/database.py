import settings
import threading
import sqlite3
import os
import utils

CURRENT_DIRPATH = os.path.dirname(__file__)
TABLES_PATH = os.path.join(CURRENT_DIRPATH, "table.sql")
DATABASE_PATH = os.path.join(settings.ROOT_DIRPATH, "data.db")


class Database:
    lock = threading.Lock()
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    conn.row_factory = lambda c, r: dict([(col[0], r[idx]) for idx, col in enumerate(c.description)])
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = true;")
    with open(TABLES_PATH) as f:
        cursor.executescript(f.read())

    def __enter__(self):
        self.lock.acquire()
        logger.debug("Lock acquired")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is None:
            self.conn.commit()
            logger.debug("Commited")
        else:
            self.conn.rollback()
            logger.warning("Rolledback")
        self.lock.release()
        logger.debug("Lock released")

    def insert(self, sql: str, **kwargs):
        try:
            self.cursor.execute(sql, kwargs)
            return self.cursor.lastrowid
        except Exception as e:
            logger.debug(sql, kwargs)
            logger.exception(e)
            raise

    def select(self, sql: str, **kwargs):
        try:
            self.cursor.execute(sql, kwargs)
            return self.cursor.fetchall()
        except Exception as e:
            logger.debug(sql, kwargs)
            logger.exception(e)
            raise

    def update(self, sql: str, **kwargs):
        try:
            self.cursor.execute(sql, kwargs)
        except Exception as e:
            logger.debug(sql, kwargs)
            logger.exception(e)
            raise

    def delete(self, sql: str, **kwargs):
        try:
            self.cursor.execute(sql, kwargs)
        except Exception as e:
            logger.debug(sql, kwargs)
            logger.exception(e)
            raise


logger = utils.get_logger(__file__)
