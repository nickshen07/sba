import sqlite3
import mysql.connector

# con = sqlite3.connect("info.db")
# cur = con.cursor()

tables = ["Tasks", "Tags", "Status", "TT"]

map = {
"Tasks":"""
CREATE TABLE IF NOT EXISTS Tasks (
    TID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name VARCHAR(255) DEFAULT 'No-Name' NOT NULL,
    Details VARCHAR(255) DEFAULT NULL,
    SID INTEGER DEFAULT 0 NOT NULL,
    DDate DATETIME,
    FOREIGN KEY (SID) REFERENCES Status(SID)
)
""",

"Tags":"""
CREATE TABLE IF NOT EXISTS Tags (
    TID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name VARCHAR(255) UNIQUE
)
""", 

"Status":"""
CREATE TABLE IF NOT EXISTS Status (
    SID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name VARCHAR(255) UNIQUE
)
""", 

"TT":"""
CREATE TABLE IF NOT EXISTS TT (
    TkID INTEGER,
    TgID INTEGER,
    PRIMARY KEY (TkID, TgID),
    FOREIGN KEY (TkID) REFERENCES Tasks(TID),
    FOREIGN KEY (TgID) REFERENCES Tags(TID)
)
"""
}

def setup():
    with sqlite3.connect("info.db") as con:
        cur = con.cursor()
        for i in tables:
            cur.execute(map[i])
        con.commit()

def reset():
    with sqlite3.connect("info.db") as con:
        cur = con.cursor()
        for i in tables:
            cur.execute(f"DROP TABLE IF EXISTS ?",i)
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

def ins(a, b):
    with sqlite3.connect("info.db") as con:
        cur = con.cursor()
        res = cur.execute("SELECT 1 FROM ? WHERE EXISTS (SELECT * FROM ? WHERE Name = ?)", (b,b,a))
        t = res.fetchall()
        if len(t)==0:
            cur.execute("INSERT INTO ? (Name) VALUES (?)", (b,a))
        con.commit()
    return ""

def init():
    with sqlite3.connect("info.db") as con:
        cur = con.cursor()
        lt = ["Not started", "On-going", "Completed", "I do not know"]
        for i in lt:
            ins(i, "Status")
        lt = ["School", "Home"]
        for i in lt:
            ins(i, "Tags")