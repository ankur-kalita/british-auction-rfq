import sqlite3
from pathlib import Path

BASE = Path(__file__).parent


def connect():
    # isolation_level=None: transactions are started explicitly with BEGIN
    conn = sqlite3.connect(BASE / "auction.db", isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init():
    conn = connect()
    conn.executescript((BASE / "schema.sql").read_text())
    conn.close()
