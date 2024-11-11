import sqlite3
import mysql.connector

con = sqlite3.connect('info.db',
                             detect_types=sqlite3.PARSE_DECLTYPES |
                             sqlite3.PARSE_COLNAMES,check_same_thread=False)
cur = con.cursor()

tables = ["Tasks", "Tags", "Statuses", "TaskTags"]

tablemap = {
"Tasks":"""
CREATE TABLE IF NOT EXISTS Tasks (
    TID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name VARCHAR(255) NOT NULL DEFAULT 'no name',
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
    TaskID INTEGER,
    TagID INTEGER,
    PRIMARY KEY (TaskID, TagID),
    FOREIGN KEY (TaskID) REFERENCES Tasks(TID),
    FOREIGN KEY (TagID) REFERENCES Tags(TID)
)
""",
}

def ins(a, b):
    q = f"SELECT 1 FROM {b} WHERE EXISTS (SELECT * FROM {b} WHERE Name = ?)"
    res = cur.execute(q, (a,))
    t = res.fetchall()
    if len(t)==0:
        q = f"INSERT INTO {b} (Name) VALUES (?)"
        cur.execute(q, (a,))
    con.commit()
    return ""

def init():
    for i in tables:
        cur.execute(tablemap[i])
    con.commit()
    lt = ["Not started", "On-going", "Completed", "I don\'t know"]
    for i in lt:
        ins(i, "Statuses")
    lt = ["School", "Home"]
    for i in lt:
        ins(i, "Tags")

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
