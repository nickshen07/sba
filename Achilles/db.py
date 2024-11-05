import sqlite3
import mysql.connector

# con = sqlite3.connect("info.db")
# cur = con.cursor()

tables = ["Tasks", "Tags", "Statuses", "TaskTags"]

map = {
"Tasks":"""
CREATE TABLE IF NOT EXISTS Tasks (
    TID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name VARCHAR(255) DEFAULT 'No-Name' NOT NULL,
    Details VARCHAR(255) DEFAULT NULL,
    SID INTEGER DEFAULT 0 NOT NULL,
    DueDate datetime,
    FOREIGN KEY (SID) REFERENCES Statuses(SID)
)
""",

"Tags":"""
CREATE TABLE IF NOT EXISTS Tags (
    TID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name VARCHAR(255) UNIQUE
)
""", 

"Statuses":"""
CREATE TABLE IF NOT EXISTS Statuses (
    SID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name VARCHAR(255) UNIQUE
)
""", 

"TaskTags":"""
CREATE TABLE IF NOT EXISTS TaskTags (
    TkID INTEGER,
    TgID INTEGER,
    PRIMARY KEY (TkID, TgID),
    FOREIGN KEY (TkID) REFERENCES Tasks(TID),
    FOREIGN KEY (TgID) REFERENCES Tags(TID)
)
"""
}

con = sqlite3.connect('info.db',
                             detect_types=sqlite3.PARSE_DECLTYPES |
                             sqlite3.PARSE_COLNAMES,check_same_thread=False)
cur = con.cursor()

def setup():
    for i in tables:
        cur.execute(map[i])
    con.commit()

def reset():
    for i in tables:
        cur.execute(f"DROP TABLE IF EXISTS {i}")
    con.commit()


def raw(query):
    cur.execute(query)
    con.commit()


def raww(query):
    res = cur.execute(query)
    res = res.fetchall()
    con.commit()
    return res

def ins(a):
    res = cur.execute("SELECT 1 FROM Statuses WHERE EXISTS (SELECT * FROM Statuses WHERE Name = ?)", (a,))
    t = res.fetchall()
    if len(t)==0:
        cur.execute("INSERT INTO Statuses (Name) VALUES (?)", (a,))
    con.commit()
    return ""

def ins2(a):
    res = cur.execute("SELECT 1 FROM Tags WHERE EXISTS (SELECT * FROM Tags WHERE Name = ?)", (a,))
    t = res.fetchall()
    if len(t)==0:
        cur.execute("INSERT INTO Tags (Name) VALUES (?)", (a,))
    con.commit()
    return ""

def init():
    lt = ["Not started", "On-going", "Completed", "I don\'t know"]
    for i in lt:
        ins(i)
    lt = ["School", "Home"]
    for i in lt:
        ins2(i)