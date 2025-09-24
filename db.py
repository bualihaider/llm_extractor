import sqlite3
from contextlib import contextmanager

DB_NAME = "analyses.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            summary TEXT,
            title TEXT,
            topics TEXT,
            sentiment TEXT,
            keywords TEXT
        )
        """)
        conn.commit()

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_NAME)
    try:
        yield conn
    finally:
        conn.close()
