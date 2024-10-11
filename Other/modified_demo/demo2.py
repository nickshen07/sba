# You can install SQLite3 Editor for Visual Studio Code to view and edit the database.
# Ref: https://marketplace.visualstudio.com/items?itemName=yy0931.vscode-sqlite3-editor

# Import the sqlite3 module
# Ref: https://docs.python.org/3/library/sqlite3.html
import sqlite3

# Connect to the SQLite database and
con = sqlite3.connect("demo.db")
cur = con.cursor()

# Enable foreign key constraints
# Ref: https://sqlite.org/foreignkeys.html
cur.execute("PRAGMA foreign_keys = ON")
con.commit()

# Drop parent and child tables if it exists
# Remark: The order of dropping tables is important to avoid foreign key constraint errors.
cur.execute("DROP TABLE IF EXISTS child")
cur.execute("DROP TABLE IF EXISTS parent")
con.commit()

# Create parent table
cur.execute(
    """
    CREATE TABLE parent (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )
    """
)
con.commit()

# Create child table with foreign key constraint to parent table
cur.execute(
    """
    CREATE TABLE child (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        parent_id INTEGER,
        name TEXT,
        age INTEGER,
        FOREIGN KEY (parent_id) REFERENCES parent(id)
    )
    """
)
con.commit()

# Insert rows into parent table
parents = [
    ("Foo",),
    ("Bar",),
]
cur.executemany("INSERT INTO parent (name) VALUES (?)", parents)
con.commit()

# Insert a row into child table
name = "Alice"
age = 3
cur.execute("INSERT INTO child (parent_id, name, age) VALUES (?, ?, ?)", (1, name, age))
con.commit()

# Insert multiple rows into child table
children = [
    (1, "Bob", 5),
    (2, "Carol", 12),
]
cur.executemany("INSERT INTO child (parent_id, name, age) VALUES (?, ?, ?)", children)
con.commit()

# Display join result of parent and child tables
res = cur.execute(
    """
    SELECT parent.name, child.name, child.age
    FROM parent
    JOIN child ON parent.id = child.parent_id
    """
)
rows = res.fetchall()
for row in rows:
    print(f"Parent: {row[0]:10} Child: {row[1]:10} Age: {row[2]:4}")
print("---END---\n")

# Error handling
# Remark: When an error occurs in the try block, the except block is executed.
#         The program continues to run after the except block without crashing.
try:
    # Insert a row with a non-existing parent_id
    cur.execute(
        "INSERT INTO child (parent_id, name, age) VALUES (?, ?, ?)",
        (3, "Dave", 15),
    )
    con.commit()
except sqlite3.Error as e:
    print(f"Error: {e}")
print("---END---\n")

# Close the database connection
con.close()