"""
db.py - MySQL connection helper (mysql-connector-python)
"""
from contextlib import contextmanager
import mysql.connector
from flask import current_app, g


def get_db():
    """Return a cached connection stored on Flask's g object."""
    if 'db' not in g:
        cfg = current_app.config
        g.db = mysql.connector.connect(
            host=cfg['MYSQL_HOST'],
            port=cfg['MYSQL_PORT'],
            user=cfg['MYSQL_USER'],
            password=cfg['MYSQL_PASSWORD'],
            database=cfg['MYSQL_DB'],
            autocommit=False,
            charset='utf8mb4',
        )
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None and db.is_connected():
        db.close()


@contextmanager
def get_cursor(dictionary=True):
    """Context manager that yields a cursor and commits/rolls back automatically."""
    db = get_db()
    cursor = db.cursor(dictionary=dictionary)
    try:
        yield cursor
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        cursor.close()


def init_app(app):
    app.teardown_appcontext(close_db)
