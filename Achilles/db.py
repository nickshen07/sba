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

def ins(a):
    with sqlite3.connect("info.db") as con:
        cur = con.cursor()
        res = cur.execute("SELECT 1 FROM Status WHERE EXISTS (SELECT * FROM Status WHERE Name = ?)", (a,))
        t = res.fetchall()
        if len(t)==0:
            cur.execute("INSERT INTO Status (Name) VALUES (?)", (a,))
        con.commit()
    return ""

def ins2(a):
    with sqlite3.connect("info.db") as con:
        cur = con.cursor()
        res = cur.execute("SELECT 1 FROM Tags WHERE EXISTS (SELECT * FROM Tags WHERE Name = ?)", (a,))
        t = res.fetchall()
        if len(t)==0:
            cur.execute("INSERT INTO Tags (Name) VALUES (?)", (a,))
        con.commit()
    return ""

def init():
    with sqlite3.connect("info.db") as con:
        cur = con.cursor()
        lt = ["Not started", "On-going", "Completed", "I do not know"]
        for i in lt:
            ins(i)
        lt = ["School", "Home"]
        for i in lt:
            ins2(i)