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
        query = f"INSERT INTO Tasks (Name) VALUES ('{task_content}')"
        try:
            setup()
            raw(query)
            return redirect('/')
        except:
            return "There was an error"
    else:
        task = raww("SELECT * FROM Tasks")
        print(task)
        return render_template('index.html', tasks = task)

@app.route('/delete/<int:id>')
def delete(id):
    try:
        query = f"DELETE FROM Tasks WHERE TID = {id}"
        print(query)
        raw(query)
        return redirect('/')
    except:
        return "There was an error"

@app.route('/update/<int:id>')
def delete(id):
    try:
        query = f"DELETE FROM Tasks WHERE TID = {id}"
        print(query)
        raw(query)
        return redirect('/')
    except:
        return "There was an error"

if __name__ == "__main__":
    app.run(debug=True)