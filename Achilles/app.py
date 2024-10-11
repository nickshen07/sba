from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from db import *
import sqlite3
import mysql.connector

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        task_content = request.form['content']
        b = 1 if 'status' in request.form else 0
        query = f"INSERT INTO Tasks (Name, Status) VALUES ('{task_content}', {b})"
        try:
            setup()
            raw(query)
            return redirect('/')
        except:
            return render_template('error.html', s="invalid input")
    else:
        task = raww("SELECT * FROM Tasks")
        print(task)
        return render_template('index.html', tasks = task)

@app.route('/delete/<int:id>')
def delete(id):
    query = f"DELETE FROM Tasks WHERE TID = {id}"
    try:
        raw(query)
        return redirect('/')
    except:
        return render_template('error.html', s="Task ID invalid")

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        b = 1 if 'status' in request.form else 0
        query = f"UPDATE Tasks SET Name = '{request.form['content']}', Status = {b} WHERE TID = {id}"
        try:
            raw(query)
            return redirect('/')
        except:
            return "There was an error"
    else:
        item = raww(f"SELECT * FROM Tasks WHERE TID = {id}")
        if len(item) == 0:
            return render_template('error.html', s="Task ID invalid")
        item = item[0]
        return render_template('update.html', item=item)

if __name__ == "__main__":
    app.run(debug=True)