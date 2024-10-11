# Import the sqlite3 module
# Ref: https://docs.python.org/3/library/sqlite3.html
import sqlite3
import mysql.connector

# Connect to the SQLite database
# You can install SQLite3 Editor for Visual Studio Code to view and edit the database.
# Ref: https://marketplace.visualstudio.com/items?itemName=yy0931.vscode-sqlite3-editor
con = sqlite3.connect("tasks.db")
cur = con.cursor()
# precreate a table if no table
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS Task (
        taskid INTEGER PRIMARY KEY AUTOINCREMENT,
        title varchar(255),
        type varchar(255),
        status BOOLEAN DEFAULT false,
        deadline DATETIME
    )
    """
)
con.commit()

def recreate():
    t = input("Would you like to delete the old one if it exists? (Y/y for yes): ")
    t = t.lower()
    if t == 'y':
        cur.execute(f"DROP TABLE IF EXISTS Task")
    else:
        print("progress cancelled")
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS Task (
            taskid INTEGER PRIMARY KEY AUTOINCREMENT,
            title varchar(255),
            type varchar(255),
            status BOOLEAN DEFAULT false,
            deadline DATETIME
        )
        """
    )
    con.commit()

# Display all tasks
def display_tasks(t):
    # Execute and fetch the results from the database
    res = cur.execute(f"SELECT * FROM {t}")
    tasks = res.fetchall()
    print(tasks)
    con.commit()

# Add a new task ()
def add_task(t, field, value):
    # Execute and commit the changes to the database
    s = f"INSERT INTO {t} ({field}) VALUES ({value})"
    # print(s)
    cur.execute(s)
    con.commit()

def del_task(tab,task):
    # Execute and commit the changes to the database
    t = input("Are you sure? (Y/y for yes): ")
    t = t.lower()
    if t == 'y':
        cur.execute(f"DELETE FROM {tab} WHERE taskid = {task}")
    else:
        print("progress cancelled")
    con.commit()

def upd_task(t, task, field, val):
    s = f"UPDATE {t} SET {field} = {val} WHERE taskid = {task}"
    cur.execute(s)
    con.commit()

def display_fields(table):
    print("List of fields:")
    p = cur.execute(f"SELECT * FROM {table}")
    for i in range(1,len(p.description)):
        print(p.description[i][0])

def display_table():
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    rows = cur.fetchall()
    if len(rows) > 0:
        print("List of tables: ")
        for i in range(len(rows)):
            print(f"{i+1}.", rows[i][0])
    else:
        recreate()
        print("There are no tables in this database, so the default table has been recreated")
    con.commit()

def del_table(id):
    t = input("Are you sure to delete the table? (Y/y for yes): ")
    t = t.lower()
    if t == 'y':
        cur.execute(f"DROP TABLE IF EXISTS {id}")
    else:
        print("progress cancelled")
    con.commit()

def add_table(name, schema):
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    rows = cur.fetchall()
    flag = 0
    for i in rows:
        if i[0]==name:
            flag = 1
    if flag == 1:
        t = input("There is a table with same name existed, would you like to delete the old one? (Y/y for yes): ")
        t = t.lower()
        if t == 'y':
            cur.execute(f"DROP TABLE IF EXISTS {name}")
        else:
            print("progress cancelled")
        cur.execute(f'CREATE TABLE IF NOT EXISTS {name} ({schema})')
    else:
        cur.execute(f'CREATE TABLE IF NOT EXISTS {name} ({schema})')
    con.commit()

def query():
    s = input("Enter the SQL command: ")
    cur.execute(s)
    t = s[:6]
    t = t.lower()
    if t == "select":
        rows = cur.fetchall()
        print("Result:")
        print(rows)