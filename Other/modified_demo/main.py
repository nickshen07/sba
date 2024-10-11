# Import the sqlite3 module
# Ref: https://docs.python.org/3/library/sqlite3.html
import sqlite3
from sbafunctions import *

import mysql.connector

# Connect to the MySQL server
# cnx = mysql.connector.connect(
#     host="localhost",
#     user="student",
#     password="12345678",
#     database="tasks",
# )
# cur = cnx.cursor()
con = sqlite3.connect("tasks.db")
cur = con.cursor()


# Connect to the SQLite database
# You can install SQLite3 Editor for Visual Studio Code to view and edit the database.
# Ref: https://marketplace.visualstudio.com/items?itemName=yy0931.vscode-sqlite3-editor

# Create database tables if they don't exist
# Ref:
# - https://www.sqlite.org/datatype3.html
# - https://sqlite.org/foreignkeys.html

# Initialize the database tables if not exist
# You can complte this step by executing the SQL queries exported from the SQLite3 Editor.

table = None

# TODO: Implement additional functions as needed before the main loop

menu = """
User menu of []:
1. Display all tasks
2. Add a task
3. Delete a task
4. Display all fields
5. Update a task
6. Change a table
7. Add a table
8. Delete a table
9. Recreate a table
10. Query a table
0. Quit
Enter your choice: 
"""

# Main loop

def main():
    while True:
        # Print user menu
        try:
            if table == None:
                display_table()
                table = input("Choose a table: ")
            try:
                # Select rows from a non-existent table
                cur.execute(f"SELECT * FROM {table}")
                rows = cur.fetchall()
                # print(f"Content of table {table}:")
                # print(rows)
            except sqlite3.OperationalError as err:
                print(f"Error: {err}")
                print("Please enter a valid table")
                table = None
                continue
            print(menu[0:15]+table+menu[15:])

            # Read user choice
            choice = input()
            while not choice.isnumeric():
                choice = input("Please input a valid integer: ")
            # Perform the selected action
            choice = int(choice)
            if choice == 1:
                print("Task list:")
                display_tasks(table)
            elif choice == 2:
                display_fields(table)
                title = input("Enter the task field(s) (without brackets): ")
                value = input("Enter the value(s) (without brackets): ")
                try:
                    add_task(table, title, value)
                except sqlite3.OperationalError as err:
                    print(f"Error: {err}")
            elif choice == 3:
                num = input("Enter the taskid: ")
                if num.isnumeric():
                    num = int(num)
                    try:
                        del_task(table, num)
                    except:
                        print("Please input a valid id")
                else:
                    print("Please input a valid integer: ")
            elif choice == 4:
                display_fields(table)
            elif choice == 5:
                task = input("Enter the task id: ")
                if not task.isnumeric():
                    print("Please input a valid integer: ")
                    continue
                task = int(task)
                field = input("Enter the field you want to update: ")
                value = input("Enter the value you want to set: ")
                upd_task(table, task, field, value)
            elif choice == 6:
                table = None
            elif choice == 7:
                name = input("Enter the name of the table: ")
                schema = input("Enter the table schema (without brackets): ")
                add_table(name, schema)
                table = None
            elif choice == 8:
                display_table()
                name = input("Choose the name of the table you want to delete: ")
                del_table(name)
                table = None
            elif choice == 9:
                recreate()
                table = "Task"
            elif choice == 10:
                query()
            elif choice == 0:
                break
            else:
                print("Invalid choice, try again")
        except Exception as e:
            print("Error (?), restart!",(e))
            table = None

    # Close the database connection
    con.close()
