import sqlite3
import mysql.connector

# con = sqlite3.connect("info.db")
# cur = con.cursor()

task = """
CREATE TABLE IF NOT EXISTS Tasks (
    TID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name VARCHAR(40) DEFAULT 'No-Name' NOT NULL,
    Status BOOLEAN DEFAULT 0
)
"""

def setup():
    with sqlite3.connect("info.db") as con:
        cur = con.cursor()
        con.execute(task)
        con.commit()

def reset():
    with sqlite3.connect("info.db") as con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS Tasks")
        con.execute(task)
        con.commit()

def raw(query):
    with sqlite3.connect("info.db") as con:
        cur = con.cursor()
        cur.execute(query)
        con.commit()

def raww(query):
    with sqlite3.connect("info.db") as con:
        cur = con.cursor()
        res = cur.execute(query)
        res = res.fetchall()
        con.commit()
    return res