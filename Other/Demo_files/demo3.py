"""
Setup MySQL Server on a Raspberry Pi

1. Ensure Raspberry Pi is up to date:
    > sudo apt update
    > sudo apt upgrade

2. Install and secure MySQL Server
    > sudo apt install default-mysql-server
    > sudo mysql_secure_installation

3. Access the database as root user
    > sudo mysql -u root -p

4. In the MySQL shell, Create a new database user
   (change username and password to your desired values)
    > CREATE USER 'username'@'localhost' IDENTIFIED BY 'password';
    > GRANT ALL PRIVILEGES ON *.* TO 'username'@'localhost' WITH GRANT OPTION;
    > FLUSH PRIVILEGES;
    > QUIT;

5. Login to the MySQL shell as the new user and create demo database
   (change username and password to your desired values)
    > mysql -u username -p
    > CREATE DATABASE demo;
    > QUIT;

6. Create a Python environment and work in it
    > python3 -m venv env
    > source env/bin/activate

7. Install the mysql-connector-python package
    > pip install mysql-connector-python

8. Run this script
    > python demo3.py
"""

# Import mysql connector
# Ref: 
# - https://dev.mysql.com/doc/connector-python/
# - https://www.w3schools.com/python/python_mysql_getstarted.asp
import mysql.connector

# Connect to the MySQL server
cnx = mysql.connector.connect(
    host="localhost",
    user="student",
    password="12345678",
    database="demo",
)
cur = cnx.cursor()

# Drop demo table if it exists
cur.execute("DROP TABLE IF EXISTS demo")
cnx.commit()

# Create demo table
# Ref: https://dev.mysql.com/doc/refman/8.0/en/data-types.html
# Remark: triple quotes are used for multi-line strings to improve readability.
cur.execute(
    """
    CREATE TABLE demo (
        id INT PRIMARY KEY AUTO_INCREMENT,
        content TEXT
    )
    """
)
cnx.commit()

# Insert a row of data
# Remark 1: The question marks (%) are the placeholders for the data to be inserted.
# Remark 2: The data is passed as a tuple matching the placeholders. If only one value
#           is to be inserted, a comma is required to indicate it is a tuple.
some_data = "Hello, World!"
cur.execute("INSERT INTO demo (content) VALUES (%s)", (some_data,))
cnx.commit()

# Insert multiple rows of data
more_data = [
    ("Sing a song of Sing Yin,",),
    ("Sing our old school song.",),
]
cur.executemany("INSERT INTO demo (content) VALUES (%s)", more_data)

# Display all rows
cur.execute("SELECT * FROM demo")
rows = cur.fetchall()
for row in rows:
    print(row)
print("---END---\n")

# Display a specific row
id = 1
cur.execute("SELECT * FROM demo WHERE id = %s", (id,))
row = cur.fetchone()
print(row)
print("---END---\n")

# Update a row
id = 1
new_content = "Hello, Sing Yin!"
cur.execute("UPDATE demo SET content = %s WHERE id = %s", (new_content, id))
cnx.commit()

# Remove a row
id = 2
cur.execute("DELETE FROM demo WHERE id = %s", (id,))
cnx.commit()

# Display all rows
cur.execute("SELECT * FROM demo")
rows = cur.fetchall()
for row in rows:
    print(row)
print("---END---\n")

# Error handling
# Ref: https://dev.mysql.com/doc/connector-python/en/connector-python-api-errors-error.html
try:
    # Select rows from a non-existent table
    cur.execute("SELECT * FROM some_table")
    rows = cur.fetchall()
except mysql.connector.Error as err:
    print(f"Error: {err}")
print("---END---\n")

# Close the database connection
cur.close()
cnx.close()