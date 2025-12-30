import sqlite3
from config import DB_PATH

with open("database/schema.sql", "r") as f:
    schema = f.read()

conn = sqlite3.connect(DB_PATH)
conn.executescript(schema)
conn.close()
