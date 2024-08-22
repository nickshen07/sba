# You can install SQLite3 Editor for Visual Studio Code to view and edit the database.
# Ref: https://marketplace.visualstudio.com/items?itemName=yy0931.vscode-sqlite3-editor

# Import the sqlite3 module
# Ref: https://docs.python.org/3/library/sqlite3.html
import sqlite3

# Connect to the SQLite database
# con - the connection object of the database and for committing changes
# cur - the cursor object for executing SQL statements
con = sqlite3.connect("demo.db")
cur = con.cursor()

# Drop demo table if it exists
cur.execute("DROP TABLE IF EXISTS demo")
con.commit()

# Create demo table
# Ref: https://sqlite.org/datatype3.html
# Remark: triple quotes are used for multi-line strings to improve readability.
cur.execute(
    """
    CREATE TABLE demo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT
    )
    """
)
con.commit()

# Insert a row of data
# Remark 1: The question marks (?) are the placeholders for the data to be inserted.
# Remark 2: The data is passed as a tuple matching the placeholders. If only one value
#           is to be inserted, a comma is required to indicate it is a tuple.
some_data = "Hello, World!"
cur.execute("INSERT INTO demo (content) VALUES (?)", (some_data,))
con.commit()

# Insert multiple rows of data
more_data = [
    ("Sing a song of Sing Yin,",),
    ("Sing our old school song.",),
]
cur.executemany("INSERT INTO demo (content) VALUES (?)", more_data)
con.commit()

# Display all rows
res = cur.execute("SELECT * FROM demo")
rows = res.fetchall()
for row in rows:
    print(row)
print("---END---\n")

# Display a specific row
id = 1
res = cur.execute("SELECT * FROM demo WHERE id = ?", (id,))
row = res.fetchone()
print(row)
print("---END---\n")

# Update a row
id = 1
new_content = "Hello, Sing Yin!"
cur.execute("UPDATE demo SET content = ? WHERE id = ?", (new_content, id))
con.commit()

# Remove a row
id = 2
cur.execute("DELETE FROM demo WHERE id = ?", (id,))
con.commit()

# Display all rows
res = cur.execute("SELECT * FROM demo")
rows = res.fetchall()
for row in rows:
    print(row)
print("---END---\n")

# Error handling
# Remark: When an error occurs in the try block, the except block is executed.
#         The program continues to run after the except block without crashing.
try:
    # Select rows from a non-existent table
    cur.execute("SELECT * FROM some_table")
    rows = cur.fetchall()
except sqlite3.Error as e:
    print("An error occurred:", e)
print("---END---\n")

# Close the database connection
con.close()